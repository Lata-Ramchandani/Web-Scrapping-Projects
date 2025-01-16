import requests as re
from bs4 import BeautifulSoup
import csv

URL = 'https://www.imdb.com/chart/top'
HEADER = {'User-Agent':'Mozilla/5.0'}
response = re.get(URL,headers=HEADER)
soup = BeautifulSoup(response.content,'html.parser')
print(response.status_code)

movies = []
for row in soup.select('.ipc-metadata-list-summary-item.sc-4929eaf6-0.DLYcv.cli-parent'):
    title = row.find('h3',class_= 'ipc-title__text').text.strip()
    year = row.find('span',class_ = 'sc-300a8231-7 eaXxft cli-title-metadata-item').text.strip('()')
    rating = row.find('span',class_ = 'ipc-rating-star--rating').text.strip()
    link = "https://www.imdb.com" + row.find('a',class_="ipc-lockup-overlay ipc-focusable")['href']
    movies.append({'title' : title, 'year' : year, 'rating' : rating, 'link' : link})

print("Top 10 Movies : ")
for movie in movies[:10]:
    print(f"{movie['title']}   {movie['year']}:    {movie['rating']}  [Link: {movie['link']}]")


# movies saved into .txt file
with open('movies.txt','w',encoding='utf-8') as file:
    for movie in movies:
        file.write(f'{movie['title']}   {movie['year']}:    {movie['rating']}  [Link: {movie['link']}]' + '\n') 