#!/usr/bin/env python3
import json
import logging
import time
from collections import namedtuple

import click
import jsondiff as jsondiff
from selenium.webdriver.support.ui import Select

from utils import create_browser, mytru_login, sendgrid_send_email, \
    read_json, write_json

Course = namedtuple('Course',
                    ['crn', 'subject', 'course', 'section', 'course_title',
                     'campus', 'final_grade', 'attempted', 'earned',
                     'gpa_hours', 'quality_points'])


def extract_final_grades(ctx, term):
    # Go to grades page
    ctx.obj.browser.get(
        'https://banssbprod.tru.ca/ssomanager/c/SSB?pkg=bwskogrd'
        '.P_ViewTermGrde')

    # Select a term
    term_selector = Select(ctx.obj.browser.find_element_by_id('term_id'))
    terms = {option.get_attribute('value'): option for option in
             term_selector.options}
    if term in terms:
        term_selector.select_by_value(term)

    ctx.obj.browser.find_element_by_id('term_id').submit()

    time.sleep(5)

    grades = ctx.obj.browser.find_elements_by_class_name('datadisplaytable')[1]

    rows = grades.find_elements_by_tag_name('tr')[1:]

    classes = []

    for row in rows:
        classes.append(Course(
            *[el.text for el in row.find_elements_by_class_name('dddefault')]))

    return classes


def format_final_grades(classes):
    return "\n".join(["{subject}{course}-{section} {title}: {grade}".format(
        subject=course.subject, course=course.course, section=course.section,
        title=course.course_title, grade=course.final_grade) for course in
        classes])


def extract_moodle_grades(browser, course_id):
    browser.get('https://moodle.tru.ca/grade/report/user/index.php?id='
                '{}'.format(course_id))

    rows = browser.find_element_by_tag_name('tr')


# TERM format
# CAMPUS: [YYYY][10|20|30] Where YYYY is the second year in the say 2017-2018
# school year
# 10 = Fall; 20 = Winter; 30 = Summer
# For OL, it's 25?
# SO YYYY is the normal number except for fall where it belongs to the next
# year

# @click.command()
# @click.option('--term', prompt='The desired term, in the format "YYYY['
#                                '10|20|25|30]"')
# @click.option('--sendgrid-api-key')
# @click.option('--email')
# @click.option('--email-from')
# def final_grades(username, password, term, sendgrid_api_key, email,
#                  email_from):
#     browser = create_browser()
#     mytru_login(browser, username, password)
#     classes = extract_final_grades(browser, term)
#     print_final_grades(classes)
#
#     if email:
#         sendgrid_send_email(sendgrid_api_key, email_from, )


class State(object):
    def __init__(self, username, password, debug=False):
        self.username = username
        self.password = password

        self.browser = create_browser(debug=debug)


@click.group()
@click.option('--username', prompt='Your Moodle/Network username')
@click.option('--password', prompt='Your Moodle/Network password')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, username, password, debug):
    ctx.obj = State(username, password, debug=debug)


@cli.command()
@click.option('--term', prompt='The term, in the format of YYYY[10|20|30]')
@click.option('--email')
@click.option('--sendgrid-api-key')
@click.option('--sender', default='noreply@mytrucli.marcolussetti.com')
@click.pass_context
def final_grades(ctx, term, email, sendgrid_api_key, sender):
    mytru_login(ctx)

    classes = extract_final_grades(ctx, term)

    old = read_json('final_grades')
    diff = jsondiff.diff(old, json.loads(json.dumps(classes)))

    if diff:
        write_json('final_grades', classes)
        click.echo("Changes detected! Current standings:\n{}".format(
            format_final_grades(classes)))

        if email:
            # Email mode detected
            if not sendgrid_api_key:
                logging.error(
                    "No api key provided for SendGrid! Please specify "
                    "a --sendgrid-api-key")
                return 1
            response = sendgrid_send_email(sendgrid_api_key,
                                           sender,
                                           email,
                                           'mytruCLI: Changes in Final '
                                           'Grades detected',
                                           "Current results:\n {}\n\n "
                                           "Difference:\n {}".format(
                                               format_final_grades(
                                                   classes),
                                               diff
                                           ))
    else:
        click.echo('No changes detected.')


if __name__ == '__main__':
    cli()
