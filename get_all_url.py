from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import json

url = 'https://2gis.ua/search/%D0%BD%D0%BE%D1%82%D0%B0%D1%80%D0%B8%D1%83%D1%81%D1%8B/rubricId/343/filters/bound?m=33.905389%2C48.826974%2F6'
browser = webdriver.Chrome(executable_path='./chromedriver')
count = 1
lst = []
browser.get(url)
time.sleep(3)
elements = browser.find_elements_by_xpath('//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div/div/div')
for a in range(1, 164):
    for i in range(1, len(elements)+1):
        try:
            url = browser.find_element_by_xpath(f'//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div/div[{i}]/div/div[2]/a')
            # time.sleep(1)
            print(url.text)
            lst.append(url.get_attribute('href'))
        except NoSuchElementException:
            print('ups')
    print(len(lst))
    if a < 7:
        element = browser.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[3]/div/div[2]')
    else:
        try:
            element = browser.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[3]/div[2]/div[2]')
        except (NoSuchElementException, KeyboardInterrupt):
            with open('./urls.json', 'w') as file:
                json.dump(lst, file)
    browser.execute_script("(arguments[0]).click();", element)
    time.sleep(5)
# webdriver.ActionChains(browser).move_to_element(element).click(element).perform()

with open('./urls.json', 'w') as file:
    json.dump(lst, file)


browser.quit()
