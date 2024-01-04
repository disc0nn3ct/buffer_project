#Чекать сайт и проверять раз в n и отправлять сообщение при >70% от макс 

import requests
# импортируем модуль
from bs4 import BeautifulSoup
import math
import time
from datetime import datetime
import random



st_accept = "text/html" # говорим веб-серверу, 
                        # что хотим получить html
# имитируем подключение через браузер Mozilla на macOS
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
# формируем хеш заголовков
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}

def check_70_percent_more(mas):
    koef = 0.6 # коэффициент от какого начинать рассылку
    # mas[1][2]
    print("len = ", len(mas)) 
    # print(mas[1][0], " = ", mas[1][1]," qq = ", mas[1][2],"   =  ",  int(mas[1][2])*0.7 )
    k=0
    min_wait = math.ceil((int(mas[1][2])*koef-int(mas[1][1]))*5)
    for i in range(1,len(mas)):
        print(i)
        wait_time = math.ceil((int(mas[i][2])*koef-int(mas[i][1]))*5)
        print(mas[i][0], " = ", mas[i][1]," qq = ", mas[i][2],"   =  ",  int(mas[i][2])*koef, " ", wait_time )
        if min_wait > wait_time:
            min_wait = wait_time
        # if(int(mas[i][1]) > int(mas[i][2])*koef):
        #     print("yes")
    
    
    # if k==0: # значит не было найдено => расчитаем сколько ждать до сл запроса 
    return min_wait # в минутах 
        


def zapros():
    req = requests.get("https://daily.heroeswm.ru/roulette/detal.php", headers)
    print("Статус ответа сайта = ", req.status_code)
    return req


    
def my_processing():
    req = zapros()
    
    soup = BeautifulSoup(req.text, "html.parser")

    # print(soup1)
    allNews = soup.find('table', class_='report', id="report_1", style="border-collapse:collapse;text-align:center", width="90%")

    #allNews = soup1.findAll('tr')

    # print(allNews)

    data = []
    table_body = allNews.find('tbody')

    data.append(['Число', 'Невыпад', 'Max', 'За_сутки'])
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    # print(data)

    # print("111 =", data[39])

    # print("qqq =",data[48])
    # Данные по числам 
    numbers_count = data[0:39]

    # Данные по дозен 
    dozen_Column = []
    dozen_Column.append(data[0])
    dozen_Column.append(data[39:49])

    Sixline = []
    Sixline.append(data[0])
    Sixline.append(data[49:61])

    Corner = []
    Corner.append(data[0])
    Corner.append(data[61:84])

    time_for_sleep = check_70_percent_more(numbers_count)

    return time_for_sleep
    


# req = requests.get("https://daily.heroeswm.ru/roulette/detal.php", headers)
# print("Статус ответа сайта = ", req.status_code)
# req = zapros



# считываем текст HTML-документа
# src = req.text
#print(src)



# # инициализируем html-код страницы 
# soup = BeautifulSoup(src, 'lxml')
# # считываем заголовок страницы
# title = soup.title.string
# # print(title)
# # Программа выведет: Курсы - Блог компании Селектел


#print(soup)




# print(Corner)

# time_for_sleep = my_processing()
# print(time_for_sleep)
# print(data[0:39])


# now = datetime.now()
# current_time = now.strftime("%H:%M:%S") 

# ожидание и перезапрос
while 1:
    time_for_sleep = my_processing()
    print(time_for_sleep)


    if time_for_sleep > 0: # todo ждать нормально до начала 5минутного промежутка 
        time.sleep(time_for_sleep * 60) 
    else:
        time.sleep(random.randint(59, 150)) 



# import pandas as pd

# # Сброс ограничений на количество выводимых рядов
# pd.set_option('display.max_rows', None)
 
# # Сброс ограничений на число столбцов
# pd.set_option('display.max_columns', None)
 
# # Сброс ограничений на количество символов в записи
# pd.set_option('display.max_colwidth', None)


# df = pd.DataFrame(data)


# # print(df)




