import telegram_send, time, requests 
from bs4 import BeautifulSoup
from pygame import mixer

site = 'https://www.amazon.co.jp/gp/product/B08XLZGY7W/ref=ppx_yo_dt_b_asin_title_o00?ie=UTF8&psc=1' #Item that we want to check
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'} #User Agent


def get_price():
    page = requests.get(site, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id='productTitle').get_text()
    price = soup.find(id='priceblock_ourprice').get_text()
    last_price = price.replace(",",".") #We are changing "," to "." for converting to float
    last_price = float(last_price[1:-1]) #We are taking out the currency symbol from the price
    last_price = last_price*1000 #Muliply by 1000 for converting price from "xx.xxx" to "xxxxx"

    if last_price < 67000: #Target price
        telegram_send.send(messages=["\U00002705 Price for RTX 3060: {}".format(price)]) #Telegram bot message.
        file = 'alert.mp3'
        mixer.init()
        mixer.music.load(file)
        mixer.music.play()


while True:
    get_price()
    time.sleep(15) #Interval