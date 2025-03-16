#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_course_main_field(course_code) -> str:
    response = requests.get(f"https://studieinfo.liu.se/kurs/{course_code}")

    if response.status_code != 200:
        return f"Failed to fetch data for {course_code}. HTTP Status: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')
    overview_section = soup.select('section.overview-content')[0]

    main_field = overview_section.contents[2].text.strip()
    
    if main_field == "":
        return "X"

    return main_field


if len(sys.argv) < 2:
    print("Usage: python scraper.py <course_code[s]>")
    sys.exit(1)

course_codes = sys.argv[1].split('\n')

results = []
with ThreadPoolExecutor() as executor:
    future_to_code = {executor.submit(
        get_course_main_field, code): code for code in course_codes}

    for future in as_completed(future_to_code):
        code = future_to_code[future]
        try:
            result = future.result()
            results.append((code, result))
        except Exception as e:
            results.append((code, f"Error fetching data: {e}"))

# Sort results by the original order of course codes
results.sort(key=lambda x: course_codes.index(x[0]))

for _, result in results:
    print(result)
