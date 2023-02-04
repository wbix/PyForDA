from urllib.request import urlopen
import webbrowser as wb
from selenium import webdriver
import time
import selenium

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import re
import csv
str = input('Введите название файла с которого считываются данные ')
def poluchenieorg(str):
    t = []
    with open(f'{str}', 'r', encoding="utf-8") as f:
        f.seek(0)
        for i in f:
            t.append(i)
    t = [line.rstrip() for line in t]
    return t
def poluchenieregistration(driver):
    driver.get('https://www.rusprofile.ru/')
    kabinet = driver.find_element(By.CLASS_NAME, 'login-tools__user-text')
    kabinet.click()
    time.sleep(0.3)
    email = driver.find_element(By.ID, 'mw-l_mail')
    email.click()
    email.send_keys('wbix@yandex.ru')
    time.sleep(0.3)
    email = driver.find_element(By.ID, 'mw-l_pass')
    email.click()
    email.send_keys('@ykDs@CNLbyG9PQ')
    time.sleep(0.3)
    parol = driver.find_element(By.ID, 'mw-l_entrance')
    parol.click()
    time.sleep(2)
    try:
        dostup = driver.find_element(By.CLASS_NAME,'btn.btn-blue-medium')
        dostup.click()
        time.sleep(3)
    except:
        pass
def search(t, driver):
    search = driver.find_element(By.NAME, 'query')
    emails=[]
    emailsnew =[]
    search.click()
    search.clear()
    search.send_keys(f'{t}')
    search.send_keys(Keys.ENTER)
    time.sleep(2)
    doc = driver.page_source
    emailsnew = re.findall(r'[\w\.-]+@[\w\.-]+', doc)
    emails.extend(emailsnew)
    emails = set(emails)
    emails = list(emails)
    if len(emails) > 10:
        emails = emails[0:10]
    return emails


def main():
    driver = webdriver.Chrome('chromedriver')
    t = poluchenieorg(str)
    poluchenieregistration(driver)
    email ={}
    for i in range(0,len(t)):
        email[f'{t[i]}'] = search(t[i],driver)
    name = input("Введите название файла в который хотите сохранить email без разширения ")
    with open(f'{name}.txt', 'w', encoding="utf-8") as file:
        for key, value in email.items():
            file.write(f'{key}, {value}\n')
    with open(f'{name}.txt', 'r', encoding='utf8') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        with open(f'{name}.csv', 'w', encoding='utf8') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('compani', 'email'))
            writer.writerows(lines)


if __name__ == '__main__':
    main()

