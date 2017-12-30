import time
from collections import namedtuple

from selenium.webdriver.support.ui import Select

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
