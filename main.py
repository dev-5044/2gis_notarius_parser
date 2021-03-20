import json
import csv
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from tqdm import tqdm
from textnorm import normalize_space


browser = webdriver.Chrome(executable_path='./chromedriver')
with open('./urls.json', 'r') as file:
    all_urls = json.load(file)


def get_name() -> str:
    name = browser.find_element_by_class_name('_oqoid').text
    return name


def get_address() -> str:
    issue = ['Це моя компанія', 'Реклама в 2GIS ↗']
    address1 = [i.text for i in browser.find_elements_by_class_name('_er2xx9') if i.text not in issue and i.text != 'Це моя компаніяРеклама в 2GIS ↗']
    address = browser.find_element_by_class_name('_1p8iqzw').text

    return ', '.join(address1) + ' ' + address


def get_schedule() -> str:
    for i in browser.find_elements_by_class_name('_z3fqkm'):
        time.sleep(1)
        browser.execute_script("(arguments[0]).click();", i)
    schedules = browser.find_element_by_class_name('_dxfma7').text
    return schedules


def get_email() -> str:
    email = browser.find_elements_by_class_name('_ke2cp9k')
    for i in email:
        if "@" in i.text:
            return i.text
        return ' '

def get_info() -> str:
    info = browser.find_element_by_class_name('_13eh3hvq').text
    return info


def get_phone() -> str:
    try:
        browser.find_element_by_class_name('_1ns0i7c').click()
    except NoSuchElementException:
        return None
    phone = browser.find_elements_by_class_name('_b0ke8')
    return ', '.join([i.text for i in phone])


def get_social() -> list:
    social = ['WhatsApp', 'Viber', 'Facebook', 'Telegram']
    web = [(i.text, i.get_attribute('href')) for i in browser.find_elements_by_class_name('_vhuumw') if i.text in social]
    return web


def parser(url) -> list:
    ''' собирает информацию о нотариусе '''
    browser.get(url)
    time.sleep(3)
    name = normalize_space(get_name())
    email = normalize_space(get_email())
    phone = normalize_space(get_phone())
    address = normalize_space(get_address())
    info = normalize_space(get_info())
    schedule = (normalize_space)
    social = normalize_space(';'.join(','.join(i) for i in get_social()))
    if schedule == 'Це моя компаніяРеклама в 2GIS ↗':
        schedule = ' '
    if address.split(',')[0] in info:
        info = ' '
    return [name, email, phone, address, info, schedule, social]


def main():
    '''записывает результат в файл'''
    head = ['name', 'email', 'phone', 'address', 'info', 'schedule', 'social']
    with open('./2gis.csv', mode='a') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(head)
        for i in tqdm(all_urls):
            file_writer.writerow(parser(i))
    browser.quit()

if __name__ == '__main__':
    main()
    
