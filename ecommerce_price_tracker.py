import requests as re
from bs4 import BeautifulSoup
import mysql.connector 
from mysql.connector import Error
import schedule 
import time 

db_config = {
    
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'password',
    'database' : 'price_tracker'
}

try:
    connection = mysql.connector.connect(**db_config)
    print("Database Successfully connected...")
except Error as error:
    print(f'Error in database connection...,{error}')

cursor = connection.cursor()

def create_table():
    query = '''CREATE TABLE  IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL, 
    url VARCHAR(500) UNIQUE,
    current_price DECIMAL(10,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''
    cursor.execute(query)
    connection.commit()

def fetch_data(url):
    response = re.get(url)
    print(f"Fetching {url}: Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f'Failed to fetch data for {url}. Status code: {response.status_code}')
        return None
    soup = BeautifulSoup(response.text,'html.parser')
    return soup

def parse_data(soup):
    try:
        product_name = soup.find ('h1',{'class' : 'css-1jjhedq e45wtet21' }).text.strip()
        product_price = soup.find('span',{'class' : 'css-95c3ey textcolor'}).text.strip()
        product_price = float(product_price.replace('₹','').replace(',',''))
        return product_name,product_price

    except AttributeError:
        print("Error Parsing in Product Data")
        return None,None
    
def save_to_database(name,url,price):
    try:
        print(f"Saving to Database {name},{url} and ₹{price}")
        query = '''INSERT INTO products(name,url,current_price)
        VALUES (%s,%s,%s)
        ON DUPLICATE KEY UPDATE current_price = %s,last_updated = NOW()'''
        cursor.execute(query,(name,url,price,price))
        connection.commit()
        print(f'Saved/Updated {name} - ₹{price}')
    except Error as error:
        print(f'Error Saving to the database: {error}')

def check_price(url,new_price):
    query = '''SELECT current_price from products WHERE url = %s'''
    cursor.execute(query,(url,))
    result = cursor.fetchone()
    if result and new_price < result[0]:
        print(f'Price Dropped for {url}. Old Price: ₹{result[0]}, New Price: ₹{new_price}')


def web_scrap(url):
    soup = fetch_data(url)
    if soup:
        name, price = parse_data(soup)
        if name and price:
            check_price(url,price)
            save_to_database(name,url,price)
    
# def schedule_scrapping():
#     urls = [
#         'https://www.caratlane.com/jewellery/ivory-heart-diamond-pendant-jp04880-1yp600.html?ef_id=CjwKCAiAm-67BhBlEiwAEVftNq0cm7_cdxM_XXmqbQfnS-edAsh37ZMyqxKYFeI4ra3xUOF0DBJgRhoCPYkQAvD_BwE:G:s&utm_campaign=Local-Inventory-Ads-Shopping--India&utm_medium=shopping_LIA_cpc&utm_source=Google&gad_source=1&gclid=CjwKCAiAm-67BhBlEiwAEVftNq0cm7_cdxM_XXmqbQfnS-edAsh37ZMyqxKYFeI4ra3xUOF0DBJgRhoCPYkQAvD_BwE'

#     ]

#     for url in urls:
#         web_scrap(url)

if __name__ == "__main__" :
    create_table()
    # schedule.every(1).hour.do(schedule_scrapping)

    # print("Price Tracker is running.....")
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    url = "https://www.caratlane.com/jewellery/ivory-heart-diamond-pendant-jp04880-1yp600.html?ef_id=CjwKCAiAm-67BhBlEiwAEVftNq0cm7_cdxM_XXmqbQfnS-edAsh37ZMyqxKYFeI4ra3xUOF0DBJgRhoCPYkQAvD_BwE:G:s&utm_campaign=Local-Inventory-Ads-Shopping--India&utm_medium=shopping_LIA_cpc&utm_source=Google&gad_source=1&gclid=CjwKCAiAm-67BhBlEiwAEVftNq0cm7_cdxM_XXmqbQfnS-edAsh37ZMyqxKYFeI4ra3xUOF0DBJgRhoCPYkQAvD_BwE"
    web_scrap(url)
    print("Web Scrapping completed....")
