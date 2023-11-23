import requests
from datetime import datetime, timedelta
import tkinter
import random

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = 'ZKQUFWU7BYZ43UK9'
API_KEY_NEWS = '56f249758c604728bad47a0f055778bb'
url_stocks = 'https://www.alphavantage.co/query'
url_news = 'https://newsapi.org/v2/everything'
params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': API_KEY
}
## STEP 1: Use https://www.alphavantage.co
yesterday = datetime.now() - timedelta(days=1)
before_yest = datetime.now() - timedelta(days=2)

response = requests.get(url_stocks, params=params)
data_yesterday = response.json()['Time Series (Daily)'][f'{yesterday.date()}']['1. open']
data_bef_yest = response.json()['Time Series (Daily)'][f'{before_yest.date()}']['4. close']

percent = round((float(data_yesterday) / float(data_bef_yest) - 1) * 100, 1)

## STEP 2: Use https://newsapi.org
parameters = {
    'q': COMPANY_NAME,
    'from': before_yest,
    'sortBy': 'popularity',
    'apikey': API_KEY_NEWS
}
response = requests.get(url_news, params=parameters)


def get_description():
    data_news = response.json()['articles'][random.randint(0, 3)]
    news_canvas.itemconfig(news_text, text=f'{STOCK}: {percent}%\n'
                                           f'\nHeadline{data_news["title"]}\n'
                                           f'\nBrief: {data_news["description"]}')


# GUI
window = tkinter.Tk()
window.title('Stock News')
window.config(width=250, height=250, bg='black', padx=50, pady=50)

stock_label = tkinter.Label(text='Stocks of TSLA', font=('Arial', 15, 'bold'), bg='orange', highlightthickness=0)
stock_label.grid(column=0, row=0)

news_canvas = tkinter.Canvas(width=300, height=300, bg='gray', highlightthickness=0)
news_text = news_canvas.create_text(150, 150, text='There will be news here.', width=290)
news_canvas.grid(column=0, row=1)

get_button = tkinter.Button(text='Get info', bg='gray', width=15, font=('Arial', 11, 'bold'),
                            command=get_description, background='orange', highlightthickness=0)
get_button.grid(column=0, row=2)
window.mainloop()
