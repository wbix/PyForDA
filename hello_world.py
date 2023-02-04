from urllib.request import urlopen
import webbrowser as wb
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv

from selenium.webdriver.support import expected_conditions as EC
import re
str = input('Введите название файла в котором расположены данные  ')
inn = input('Параметр поиска(пример: 1.ИНН 2.Название  ').lower()
def poluchenieorg(str):
    t = []
    with open(f'{str}', 'r', encoding="utf-8") as f:
        f.seek(0)
        for i in f:
            t.append(i)
    t = [line.rstrip() for line in t]
    return t
def poluchenielinkfororg(t,driver, inn):
    for i in range(0,1):
        if  inn != 'инн':
            inn = ' '
        driver.get('https://www.google.ru/')
        org_name = driver.find_element(By.NAME, 'q')
        org_name.click()
        org_name.send_keys(f'{inn}{t} компания')
        org_name.send_keys(Keys.ENTER)
        time.sleep(2)
        driver.implicitly_wait(2)
        urllink = driver.find_elements(By.CLASS_NAME, 'yuRUbf')
        lang_link1 = []
        lang_link2 = []
        for elem in urllink:
            lang_link1.append(elem.get_attribute('innerHTML'))
        for i in lang_link1:
            count = 0
            ind1 = -1
            ind2 = -1
            for j in i:

                if j== '"' and ind1 == -1 and count !=0:
                    ind1 = count
                    continue
                if j == '"' and ind1 != -1:
                    ind2 = count
                count += 1
                if ind1 != -1 and ind2 != -1:
                    lang_link2.append(i[ind1+1: ind2+1])
                    break
        #ссылки на сайты
        lang_link2 = lang_link2[0:5]
        return lang_link2
def poluchenieemail(link, driver):
    emails = []
    emailsnew = []
    for t in range(0, len(link)):
        try:
            driver.get(f'{link[t]}')
            doc = driver.page_source
            emailsnew = re.findall(r'[\w\.-]+@[\w\.-]+', doc)

        except:
            pass
        emails.extend(emailsnew)
    emails = set(emails)
    emails = list(emails)
    if len(emails)>10:
        emails = emails[0:10]
    return emails
def main():
    driver = webdriver.Chrome('chromedriver')
    t = poluchenieorg(str)
    email = {}
    for i in range(0, len(t)):
        link = poluchenielinkfororg(t[i], driver, inn)
        email[f'{t[i]}'] = poluchenieemail(link, driver)
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

