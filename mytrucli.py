#!/usr/bin/env python3
import json
import logging

import click
import jsondiff as jsondiff
from tabulate import tabulate

import mytru
import moodle
from utils import create_browser, sendgrid_send_email, read_json, \
    write_json, end


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
    def __init__(self, username, password, email=None, sendgrid_api_key=None,
                 sender=None, debug=False):
        self.username = username
        self.password = password
        self.sendgrid_api_key = sendgrid_api_key
        self.sender = sender
        self.email = email

        self.browser = create_browser(debug=debug)


@click.group()
@click.option('--username', prompt='Your Moodle/Network username')
@click.option('--password', prompt='Your Moodle/Network password')
@click.option('--email', default=None)
@click.option('--sendgrid-api-key', default=None)
@click.option('--sender', default='noreply@mytrucli.marcolussetti.com')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, username, password, email, sendgrid_api_key, sender, debug):
    ctx.obj = State(
        username, password, email=email,
        sendgrid_api_key=sendgrid_api_key, sender=sender, debug=debug)


@cli.command()
@click.option('--term', prompt='The term, in the format of YYYY[10|20|30]')
@click.pass_context
def final_grades(ctx, term):
    mytru.login(ctx)

    classes = mytru.extract_final_grades(ctx, term)

    old = read_json('final_grades')
    diff = jsondiff.diff(old, json.loads(json.dumps(classes)))

    if diff:
        write_json('final_grades', classes)
        click.echo("Changes detected! Current standings:\n{}".format(
            mytru.format_final_grades(classes)))

        if ctx.obj.email:
            # Email mode detected
            if not ctx.obj.sendgrid_api_key:
                logging.error(
                    "No api key provided for SendGrid! Please specify "
                    "a --sendgrid-api-key")
                end(ctx, status=1)
            response = sendgrid_send_email(
                ctx.obj.sendgrid_api_key,
                ctx.obj.sender,
                ctx.obj.email,
                'mytruCLI: Changes in Final Grades detected',
                "Current results:\n {}\n\n Difference:\n {}".format(
                    mytru.format_final_grades(classes), diff))
    else:
        click.echo('No changes detected.')

    end(ctx, status=0)


@cli.command()
@click.option('--course', prompt='Course number, as in the moodle id')
@click.pass_context
def moodle_grades(ctx, course):
    moodle.login(ctx)

    headers, grades = moodle.extract_grades(ctx, course)

    old = read_json('moodle_grades_{}'.format(course))
    diff = jsondiff.diff(old, json.loads(json.dumps(grades)))

    if diff:
        write_json('moodle_grades_{}'.format(course), grades)
        click.echo("Changes detected! Current standings:\n{}".format(
            tabulate(grades, headers=headers)))

        if ctx.obj.email:
            # Email mode detected

            # Craft email
            text = """
            Dear user,
            Changes have been detected in your grades for course {course}.

            Here are your current grades:
            {table}

            Regards,
            myTruCLI
            """
            html = """
            <html><body><p>Dear user,</p>
            <p>Changes have been detected in your grades for course {course}.</p>
            <p>Here are your current grades:</p>
            {table}
            <p>Regards,</p>
            <p>myTruCLI</p>
            </body></html>
            """

            text = text.format(
                course=course,
                table=tabulate(grades, headers=headers, tablefmt='grid'))
            html = html.format(
                course=course,
                table=tabulate(grades, headers=headers, tablefmt='html')
            )

            # Send email
            if not ctx.obj.sendgrid_api_key:
                logging.error(
                    "No api key provided for SendGrid! Please specify "
                    "a --sendgrid-api-key")
                end(ctx, status=1)
            response = sendgrid_send_email(
                ctx.obj.sendgrid_api_key,
                ctx.obj.sender,
                ctx.obj.email,
                'mytruCLI: Changes in Moodle Grades detected for class {'
                '}'.format(course),
                html)
    else:
        click.echo('No changes detected.')
    # text = "\n".join([" | ".join(row) for row in grades])
    # text = tabulate(grades, headers=headers)
    #
    # click.echo(text)

    end(ctx, status=0)


@cli.command()
@click.option('--course', prompt='Course number, as in the moodle id')
@click.pass_context
def moodle_assignments(ctx, course):
    moodle.login(ctx)

    headers, assignments = moodle.extract_assignments(ctx, course)

    text = tabulate(assignments, headers=headers)

    click.echo(text)

    end(ctx, status=0)


if __name__ == '__main__':
    cli()
