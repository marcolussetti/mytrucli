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
