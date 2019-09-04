#!/usr/bin/python
# -*- coding: utf8 -*-
'''
The Scrip is Right, but I have static ip address and I could not change self ip address
'''
import csv
import xlwt
import xlrd
import time
import xlutils
import requests
import numpy as np
from bs4 import BeautifulSoup
import matplotlib as plt
import sklearn as nn


def get_html_ip_site(url_ip_site):
    r_ip_site = requests.get(url_ip_site)
    return r_ip_site.text

def get_html_avito_site(url_avito_site):
    r_avito_site = requests.get(url_avito_site)
    return r_avito_site.text

def get_html_spy_site(url_spy_site, useragent=None, proxy=None):
    r_spy_site = requests.get(url_spy_site, headers=useragent, proxies=proxy, timeout=10)
    return r_spy_site.text


def get_ip(html_spy_site):
    print('New Proxy & User-Agent:')
    soup = BeautifulSoup(html_spy_site, 'lxml')
    print('\n\n\n---------------------------')
    ip = soup.find('span', class_='ip').text.strip()
    ua = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip)
    print(ua)
    print('---------------------------')


def read_xls_avito():
    MAX_COUNT_ROWS = 260  # max count rows in on sheet
    MAX_ROWS = 270  # max value of rows in on sheet
    MAX_COLS = 50.  # max value of cols in on sheet
    rb = xlrd.open_workbook('avito.xls', formatting_info=True)
    sheet = rb.sheet_by_index(1)

    for rownum in reversed(range(sheet.nrows)):
        cell = sheet.cell(rownum, 1)
        axis_y = np.insert(axis_y, 1, cell.value)

def write_csv_ip(free_ip):
    with open('free_ip.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((free_ip['free_ip']))
    f.close();


def write_csv_avito(data):              # UNUSED
    with open('avito.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['km'],
                         data['url']))
    f.close();


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='pagination-pages clearfix')
    pages = divs.find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def get_page_data(html_ip_site):
    f = open('free_ip.csv', 'w')
    f.close();
    soup = BeautifulSoup(html_ip_site, 'lxml')

    table_body = soup.find('table')
    rows = table_body.find_all('tr')

    free_data_ip = []
    for row in rows:
        ips = row.find_all('td')
        free_ip = [(ele.text.strip()) for ele in ips][:1]
        free_ips = {'free_ip': free_ip}
        write_csv_ip(free_ips)

        free_data_ip += free_ip

    return free_data_ip


def get_page_data_in_avito(html, sheet, index):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='catalog-list')
    ads = divs.find_all('div', class_='item_table')

    for ad in ads:
        try:
            div = ad.find('div', class_='description').find('h3')
            if '2-к квартира' not in div.text.lower():
                continue
            else:
                title = div.text.strip()
        except:
            title = ''
        try:
            div = ad.find('div', class_='description').find('h3')
            url = "https://avito.ru" + div.find('a').get('href')
        except:
            url = ''
        try:
            price = ad.find('div', class_='about').text.strip()
        except:
            price = ''
        try:
            div = ad.find('p', class_='address')
            km = div.find('span', class_='c-2').text.strip()
        except:
            metro = ''
            km = ''
        data = {'title': title,
                'price': price,
                'km': km,
                'url': url}
        sheet.write(index, 0, data['title'])
        sheet.write(index, 1, data['price'])
        sheet.write(index, 2, data['km'])
        sheet.write(index, 3, data['url'])
        index += 1
    return index

def change_ip():
    url_spy_site = 'http://sitespy.ru/my-ip'
    url_ip_site = 'https://www.ip-adress.com/proxy-list'

    html_ip_site = get_html_ip_site(url_ip_site)

    proxiess = get_page_data(html_ip_site)
    useragents = open('useragents.txt').read().split('\n')

    for i in range(3):
        proxy = {'http': 'http://'+ proxiess[np.random.randint(len(proxiess))]}
        useragent = {'User-Agent': useragents[np.random.randint(len(useragents))]}

        try:
            html_spy_site = get_html_spy_site(url_spy_site, useragent, proxy)
        except:
            continue
        get_ip(html_spy_site)



def main():
    book_avito = xlwt.Workbook()
    sheet = book_avito.add_sheet('Avito')
    index = 0

    url_avito_site = "https://www.avito.ru/sankt-peterburg/kvartiry/prodam/2-komnatnye/novostroyka"
    base_url_avito_site = "https://www.avito.ru/sankt-peterburg/kvartiry/prodam/2-komnatnye/novostroyka?"
    page_part_avito_site = "p="
    query_par_avito_site = "&f=59_13989b?"

    total_pages = get_total_pages(get_html_avito_site(url_avito_site))

    for i in range(1, total_pages):       # 100 is maximum
        url_gen = base_url_avito_site + page_part_avito_site + str(i) + query_par_avito_site

        time.sleep(3 * np.random.random_sample() + 3)  # [3, 6): (b - a) * random_sample() + a
        try:
            html_avito_site = get_html_avito_site(url_gen)
        except:
            change_ip()
        index = get_page_data_in_avito(html_avito_site, sheet, index)
    book_avito.save('avito.xls')



if __name__ == '__main__':
    main()
