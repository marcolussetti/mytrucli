import time

import sendgrid
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from sendgrid.helpers.mail import *


def create_browser(debug=False):
    # Setup browser
    options = Options()
    if not debug:
        options.add_argument('-headless')
    browser = webdriver.Firefox(firefox_options=options)

    return browser


#def mytru_login(browser, username, password):
def mytru_login(ctx):
    # Log in to TRU
    ctx.obj.browser.get('http://trustudent.tru.ca')
    ctx.obj.browser.find_element_by_id('username').send_keys(ctx.obj.username)
    ctx.obj.browser.find_element_by_id('password').send_keys(ctx.obj.password)
    ctx.obj.browser.find_element_by_id('password').submit()

    # Wait for all the slow redirects to work
    time.sleep(5)


def moodle_login(browser, username, password):
    # Log in to Moodle
    browser.get('https://moodle.tru.ca')
    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('password').send_keys(password)
    browser.find_element_by_id('password').submit()

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
