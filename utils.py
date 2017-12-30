import json
import os
import time

import sendgrid
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from sendgrid.helpers.mail import *


CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.mytrucli')


def create_browser(debug=False):
    # Setup browser
    options = Options()
    if not debug:
        options.add_argument('-headless')
    browser = webdriver.Firefox(firefox_options=options)

    return browser


def mytru_login(ctx):
    # Log in to TRU
    ctx.obj.browser.get('http://trustudent.tru.ca')
    ctx.obj.browser.find_element_by_id('username').send_keys(ctx.obj.username)
    ctx.obj.browser.find_element_by_id('password').send_keys(ctx.obj.password)
    ctx.obj.browser.find_element_by_id('password').submit()

    # Wait for all the slow redirects to work
    time.sleep(5)


def moodle_login(ctx):
    # Log in to Moodle
    ctx.obj.browser.get('https://moodle.tru.ca')
    ctx.obj.browser.find_element_by_id('username').send_keys(ctx.obj.username)
    ctx.obj.browser.find_element_by_id('password').send_keys(ctx.obj.password)
    ctx.obj.browser.find_element_by_id('password').submit()

    time.sleep(5)


def sendgrid_send_email(api_key, from_email, to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(apikey=api_key)
    mail = Mail(
        Email(from_email),
        subject,
        Email(to_email),
        Content("text/plain", content)
    )

    return sg.client.mail.send.post(request_body=mail.get())


def read_json(file_name):
    file_path = os.path.join(CONFIG_DIR, "{}.json".format(file_name))
    if os.path.isfile(file_path):
        with open(file_path) as f:
            return json.load(f)
    else:
        return None


def write_json(file_name, data):
    file_path = os.path.join(CONFIG_DIR, "{}.json".format(file_name))
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    with open(file_path, 'w') as f:
        json.dump(data, f)


def end(ctx, status=0):
    if ctx.obj.browser:
        ctx.obj.browser.quit()
    return status


# def compare_json():
