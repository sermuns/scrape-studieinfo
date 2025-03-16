#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import sys


def get_course_main_field(course_code) -> str:
    response = requests.get(f"https://studieinfo.liu.se/kurs/{course_code}")

    if response.status_code != 200:
        print(f"Failed to fetch data. HTTP Status: {response.status_code}")
        sys.exit(0)

    soup = BeautifulSoup(response.text, 'html.parser')
    overview_section = soup.select('section.overview-content')[0]

    return overview_section.contents[2].text.strip()


if len(sys.argv) < 2:
    print("Usage: python scraper.py <course_code[s]>")
    sys.exit(1)

course_codes = sys.argv[1].split('\n')
print(course_codes)

for course_code in course_codes:
    print(get_course_main_field(course_code))
