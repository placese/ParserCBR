import csv
import datetime

import matplotlib
import matplotlib.pyplot as plt

from parser import FILE

matplotlib.style.use('ggplot')


def create_graphic():
    course = read_file(FILE)
    x = []
    y = []
    x2 = []
    y2 = []
    x3 = []
    y3 = []
    for i in course:
        x.append(datetime.datetime.strptime(i['Date'], "%Y-%m-%d").date())
        y.append(i['Coefficient'])

    sum_100 = get_sma(course, 100)
    sum_10 = get_sma(course, 10)

    ctr = 0
    for i in course[:course.__len__()-100:100]:
        x2.append(datetime.datetime.strptime(i['Date'], "%Y-%m-%d").date())
        y2.append(sum_100[ctr])
        ctr += 1

    ctr = 0
    for i in course[:course.__len__()-10:10]:
        x3.append(datetime.datetime.strptime(i['Date'], "%Y-%m-%d").date())
        y3.append(sum_10[ctr])
        ctr += 1


    plt.figure(figsize=(15, 7))
    plt.plot(x, y, label='Rate')
    plt.plot(x2, y2, label='100 days SMA')
    plt.plot(x3, y3, label='10 days SMA')
    plt.gca().spines["top"].set_alpha(0.0)
    plt.gca().spines["bottom"].set_alpha(0.3)
    plt.gca().spines["right"].set_alpha(0.0)
    plt.gca().spines["left"].set_alpha(0.3)
    plt.title("USD rate")
    plt.legend()
    plt.show()


def get_sma(course, n):
    result_sma = []
    p = n
    sum = 0
    m = 0
    ctr = 0
    for i in course[::n]:
        ctr += 1
    for j in range(ctr):
        for i in course[m:n:]:
            sum += i['Coefficient']
        sum /= p
        result_sma.append(sum)
        sum = 0
        m = n
        n += p
    result_sma.pop(result_sma.__len__()-1)
    return result_sma


def read_file(path):
    with open(path, 'r', newline='') as file:
        course = []
        reader = csv.DictReader(file, delimiter=';')
        for line in reader:
            course.append({
                'Date': line['Date'],
                'Coefficient': float(line['Coefficient'])
            })
    return course


if __name__ == '__main__':
    create_graphic()
