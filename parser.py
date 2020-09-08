from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import csv

END_DATE = datetime.today().date().strftime("%d.%m.%Y")
START_DATE = datetime.today().date().replace(year=datetime.today().date().year - 5).strftime("%d.%m.%Y")

URL = f"https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.mode=1&UniDbQuery.date_req1" \
      f"=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01235&UniDbQuery.From={START_DATE}&UniDbQuery.To={END_DATE}"
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0',
           'accept': '*/*'}
FILE = 'course.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr')

    course_tmp = []
    for item in items:
        item = item.find_all('td')
        course_tmp.append({
            'item': item
        })
    del course_tmp[0]
    del course_tmp[0]

    course = []
    for i in range(course_tmp.__len__()):
        course.append({
            'Date': re.findall('\d{2}[.]\d{2}[.]\d{4}', str(course_tmp[i].get('item'))),
            'Coefficient': str(re.findall('\d{2}[,]\d{4}', str(course_tmp[i].get('item')))).replace(',', '.')
        })
    return course


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Date', 'Coefficient'])
        for item in items:
            date_obj = datetime.strptime(
                str(item['Date']).replace('[', '').replace(']', '').replace('\'', '').replace('\'', ''),
                '%d.%m.%Y')
            coefficient = float(
                str(item['Coefficient']).replace('[', '').replace(']', '').replace('\'', '').replace('\'', ''))
            writer.writerow([date_obj.date(), coefficient])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        course = get_content(html.text)
        # get_content(html.text)
        save_file(course, FILE)
        if __name__ == '__main__':
            print(course)
    else:
        raise Exception("error")


if __name__ == '__main__':
    parse()
