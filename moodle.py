import time


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
                [el.text for el in row.find_elements_by_tag_name('td')]
            )
        else:
            output.append([row.text])

    return headers, output
