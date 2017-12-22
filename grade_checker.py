#!/usr/bin/env python3

import time
from collections import namedtuple

import click
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select

Course = namedtuple('Course',
                    ['crn', 'subject', 'course', 'section', 'course_title',
                     'campus', 'final_grade', 'attempted', 'earned',
                     'gpa_hours', 'quality_points'])


def create_browser():
    # Setup browser
    options = Options()
    options.add_argument('-headless')
    browser = webdriver.Firefox(firefox_options=options)

    return browser


def mytru_login(browser, username, password):
    # Log in to TRU
    browser.get('http://trustudent.tru.ca')
    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('password').send_keys(password)
    browser.find_element_by_id('password').submit()

    # Wait for all the slow redirects to work
    time.sleep(5)


def extract_final_grades(browser, term):
    # Go to grades page
    browser.get(
        'https://banssbprod.tru.ca/ssomanager/c/SSB?pkg=bwskogrd.P_ViewTermGrde')

    # Select a term
    term_selector = Select(browser.find_element_by_id('term_id'))
    terms = {option.get_attribute('value'): option for option in
             term_selector.options}
    if term in terms:
        term_selector.select_by_value(term)

    browser.find_element_by_id('term_id').submit()

    time.sleep(5)

    grades = browser.find_elements_by_class_name('datadisplaytable')[1]

    rows = grades.find_elements_by_tag_name('tr')[1:]

    classes = []

    for row in rows:
        classes.append(Course(
            *[el.text for el in row.find_elements_by_class_name('dddefault')]))

    return classes


def print_final_grades(classes):
    print("\n".join(["{subject}{course}-{section} {title}: {grade}".format(
        subject=course.subject, course=course.course, section=course.section,
        title=course.course_title, grade=course.final_grade) for course in
        classes]))


# TERM format
# CAMPUS: [YYYY][10|20|30] Where YYYY is the second year in the say 2017-2018
# school year
# 10 = Fall; 20 = Winter; 30 = Summer
# For OL, it's 25?
# SO YYYY is the normal number except for fall where it belongs to the next
# year

@click.command()
@click.option('--username', prompt='Your Moodle/Network username')
@click.option('--password', prompt='Your Moodle/Network password')
@click.option('--term', prompt='The desired term, in the format "YYYY['
                               '10|20|25|30]"')
def final_grades(username, password, term):
    browser = create_browser()
    mytru_login(browser, username, password)
    classes = extract_final_grades(browser, term)
    print_final_grades(classes)


if __name__ == '__main__':
    final_grades()
