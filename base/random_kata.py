import argparse
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options


class DataBase(dict):
    def __init__(self):
        self._file = Path('kata.db')
        self._file.touch(exist_ok=True)
        with open(self._file, 'r') as file:
            d = {}
            for line in file:
                url, week = line.split(',')
                d[url] = week.strip()
            self.__dict__.update(d)
    
    @property
    def date_dict(self):
        return {v: k for k, v in self.__dict__.items()}

    def update(self, url):
        date = datetime.now()
        if f'{date:%g_%U}' in self.date_dict:
            raise KeyError('already a kata for this date in database')
        with open(self._file, 'a') as file:
            file.write(f'{url},{date:%g_%U}\n')


DB = DataBase()

BASE = 'https://www.codewars.com'

def find_new_kata(kyu: int = 7):
    if kyu < 1 or kyu > 8:
        raise ValueError('kyu is expected to be between 8 and 1')

    params = {'r[]':-1*kyu,
              'beta': False,
              'order_by': 'satisfaction_percent',
              'sample': True,
              }
    
    new_katas = {}
    while not new_katas:
        search = requests.get(BASE + '/kata/search/python', params=params)
        search_soup = BeautifulSoup(search.content, features='html.parser')

        katas = search_soup.findAll('a', attrs={'class':'ml-2'})
        found_katas = {kata.get('href') for kata in katas}
        new_katas = found_katas - DB.keys()

    new_kata, *_ = new_katas
    return new_kata


def get_kata(kata: str) -> str:
    """Return a HTML string from the the katas description."""

    description = requests.get(BASE + kata + '/train/python')

    options = Options()
    options.headless = True
    with webdriver.Firefox(options=options) as driver:
        driver.get(BASE + kata + '/train/python')
        WebDriverWait(driver, timeout=10).until(
                lambda d: len(d.find_element(By.ID, 'description').text) > 30)
        exercise = driver.page_source
        return exercise


def create_description(html: str):
    """Create a markdown description from the kata website."""
    exercise = BeautifulSoup(html)
    
    description = exercise.find('div', attrs={'id': 'description'})
    tests = extract_tests(exercise)
    doctests = [f'>>> solution({args})\n{expected}' for args, expected in tests]


def extract_tests(soup: BeautifulSoup) -> list[str]:
    """Extract input arguments and return value from kata description."""

    attrs = {'class': 'CodeMirror-line', 'role': 'presentation'}
    tests = (test.text for test in soup.findAll('pre', attrs=attrs)
                if 'assert_equals' in test.text)

    test_cases = [split_test(case) for case in tests]
    return test_cases


def split_test(test: str) -> tuple[str, str]:
    """Clean up the raw test strings into argument and return value."""

    _test_call, test_arguments = test.split('assert_equals')
    clean_args = test_arguments[1:-1]
    _function, args = clean_args.split('(', maxsplit=1)

    count = 1
    counter = {'(': 1, ')': -1}
    for n, char in enumerate(args):
        count += counter.get(char, 0)
        if count == 0:
            break
    else:
        raise ValueError(f'Input: {test} could not be processed')
    
    provided = args[:n]
    try:
        _, expected = args[n:].split(',')  # , separates provided and expected
    except ValueError:
        _, expected, *rest = args[n:].split(',')
        expected = expected + '  # ' + ' '.join(rest)
    
    expected = expected.strip()
    return provided, expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--kyu', type=int, default=6)
    parser.add_argument('--url', type=str, default=None)

    args = parser.parse_args()
    
    if not args.url:
        kata = find_new_kata(args.kyu)
    else:
        kata = '/kata/' + args.url

    html = get_kata(kata)
    exercise = BeautifulSoup(html, features='html.parser')
    description = exercise.find('div', attrs={'id': 'description'})
    tests = extract_tests(exercise)
    doctests = [f'>>> solution({args})\n{expected}' for args, expected in tests]

    text = [description.text]
    text.append('```python')
    text.extend(doctests)
    text.append('```')
    print('\n'.join(text))

    DB.update(kata)


if __name__ == '__main__':
    main()
