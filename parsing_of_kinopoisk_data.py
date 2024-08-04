import requests
from bs4 import BeautifulSoup
import pandas as pd
import config
from config import user_id

# with open('kinopoisk.html', 'w', encoding='utf-8') as output_file:
#    output_file.write(r.text)

def collect_rates(user_id):
   page_num = 1
   data = []

   while True:
       url = f'https://www.kinopoisk.ru/user/{user_id}/votes/list/vs/vote/page/{page_num}/#list'
       html_content = requests.get(url).text

       soup = BeautifulSoup(html_content, 'lxml')

       entries = soup.find_all('div', class_='item')

       if len(entries) == 0:  # Признак остановки
           break

       for entry in entries:
    #записываем названия фильмов
           item_info = entry.find('div', class_='info')
           name_rus = item_info.find('div', class_='nameRus')
           film_name = name_rus.find('a').text
    #записываем рейтинг фильма от кинопоиска
           rating = item_info.find('div', class_='rating')

           b_element = rating.find('b')
           if b_element is not None:
               kinopoisk_rating = float(b_element.text)
           else:
               kinopoisk_rating = None
    #записываем оценку фильма от пользователя
           vote = entry.find('div', class_='vote').text

           data.append({'film_name': film_name, 'kinopoisk_rating': kinopoisk_rating, 'user rating': vote})
       page_num += 1
   return data

#print(collect_rates('2057575'))
rating_table = collect_rates(config.user_id)
print(len(rating_table))
df = pd.DataFrame(rating_table)

df.to_excel('rating_table.xlsx')
