#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import re


def get_rivals(course_code) -> str:

    # if coursecode not matchign regex
    if not re.match(r'[A-Za-z]{4}\d{2}', course_code):
        return ""

    response = requests.get(
        f"https://studieinfo.liu.se/kurs/{course_code}")

    if response.status_code != 200:
        return f"Failed to fetch data for {course_code}. HTTP Status: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')
    syllabus = soup.select_one('div#syllabus section')

    special_info = syllabus.find('h2', string='Särskild information')

    if not special_info:
        # return f"No special information found for {course_code}"
        return ''

    special_text = special_info.find_next_sibling('p').text

    # extract coursecodes from text
    coursecodes = re.findall(r'[A-Za-z]{4}\d{2}', special_text)

    # remove duplicates
    coursecodes = list(set(coursecodes))

    # reutnr as string comma separated
    return ', '.join(coursecodes)


if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <course_code[s]>")
    sys.exit(1)

course_codes = sys.argv[1].split('\n')

results = []
with ThreadPoolExecutor() as executor:
    future_to_code = {executor.submit(
        get_rivals, code): code for code in course_codes}

    for future in as_completed(future_to_code):
        code = future_to_code[future]
        try:
            result = future.result()
            results.append((code, result))
        except Exception as e:
            results.append((code, f"Error fetching data: {e}"))

# Sort results by the original order of course codes
results.sort(key=lambda x: course_codes.index(x[0]))

# print('---')
for _, result in results:
    print(result)
