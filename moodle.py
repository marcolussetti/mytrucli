import re
import time
from collections import namedtuple

import dateparser as dateparser

Assignment = namedtuple('Assignment',
                        ['id', 'title', 'url', 'due_date', 'grade'])


def login(ctx):
    # Log in to Moodle
    ctx.obj.browser.get('https://moodle.tru.ca')
    ctx.obj.browser.find_element_by_id('username').send_keys(ctx.obj.username)
    ctx.obj.browser.find_element_by_id('password').send_keys(ctx.obj.password)
    ctx.obj.browser.find_element_by_id('password').submit()

    time.sleep(5)


def extract_grades(ctx, course_id):
    ctx.obj.browser.get('https://moodle.tru.ca/grade/report/user/index.php?id='
                        '{}'.format(course_id))

    rows = ctx.obj.browser.find_elements_by_tag_name('tr')

    # Grade = namedtuple(
    #     'Grade',
    #     [stringcase.snakecase(el.text) for el
    #      in rows[0].find_elements_by_tag_name('th')])
    #
    # level_regex = re.compile(r'level(\d+)')
    # max_level = max(
    #     [re.search(
    #         level_regex,
    #         row.find_element_by_tag_name('th').get_attribute('class')
    #     ).group(1)
    #      for row in rows[1:]])

    headers = [el.text for el in rows[0].find_elements_by_tag_name('th')]

    output = []

    for row in rows[1:]:
        if len(row.find_elements_by_tag_name('td')) > 1:
            # Grade row
            output.append(
                [row.find_element_by_tag_name('th').text] +
                [el.text for el in row.find_elements_by_tag_name('td')]
            )
        else:
            output.append([row.text])

    return headers, output


def extract_assignments(ctx, course_id):
    ctx.obj.browser.get('https://moodle.tru.ca/mod/assign/index.php?id='
                        '{}'.format(course_id))

    rows = ctx.obj.browser.find_elements_by_tag_name('tr')

    # Grade = namedtuple(
    #     'Grade',
    #     [stringcase.snakecase(el.text) for el
    #      in rows[0].find_elements_by_tag_name('th')])
    #
    # level_regex = re.compile(r'level(\d+)')
    # max_level = max(
    #     [re.search(
    #         level_regex,
    #         row.find_element_by_tag_name('th').get_attribute('class')
    #     ).group(1)
    #      for row in rows[1:]])

    headers = [el.text for el in rows[0].find_elements_by_tag_name('th')]

    output = []

    for row in rows[1:]:
        if len(row.find_elements_by_tag_name('td')) > 1:
            # Grade row
            output.append(
                [el for el in row.find_elements_by_tag_name('td')]
            )

    records = []

    for row in output:
        record = {}
        if headers.index('Assignments'):
            record['title'] = row[headers.index('Assignments')].text.strip()
            record['url'] = row[
                headers.index('Assignments')].find_element_by_tag_name(
                'a').get_attribute('href')
            record['id'] = re.search("([0-9]+)", record['url']).groups()[0]
        else:
            continue

        if headers.index('Due date') and row[headers.index(
                'Due ' 'date')].text.strip():
            record['due_date'] = dateparser.parse(
                row[headers.index('Due date')].text,
                settings={'TIMEZONE': 'America/Vancouver'})
        else:
            record['due_date'] = None

        if headers.index('Grade'):
            record['grade'] = row[headers.index('Grade')].text
        else:
            record['grade'] = None

        records.append(Assignment(**record))

    headers = Assignment._fields

    return headers, records
