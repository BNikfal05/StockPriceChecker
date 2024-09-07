import requests
import datetime as dt

NEWS_API_KEY = "YOUR KEY"
NEWS_API_URL='https://newsapi.org/v2/top-headlines'
News_api_paramters = {
    'apiKey': NEWS_API_KEY,
    'country': 'us',
    'category': 'business',
    'q': 'NVidia Stocks'
}

AV_API_KEY = "YOUR KEY"
AV_API_URL = "https://www.alphavantage.co/query"
AV_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "NVDA",
    "apikey": AV_API_KEY
}

# Fetching News for Stock
response1 = requests.get(url=NEWS_API_URL, params=News_api_paramters)
response1.raise_for_status()
today_news_data = response1.json()

# Setting up the time
today = dt.datetime.now() -dt.timedelta(days=2)
yesterday = today - dt.timedelta(days=3)
today_str = today.strftime("%Y-%m-%d")
yesterday_str = yesterday.strftime("%Y-%m-%d")


# Getting Stock Data
response = requests.get(url=AV_API_URL, params=AV_parameters)
response.raise_for_status()
data = response.json()
stock_value_today = float(data["Time Series (Daily)"][today_str]['4. close'])
stock_value_yesterday = float(data["Time Series (Daily)"][yesterday_str]['4. close'])

daily_difference = stock_value_today - stock_value_yesterday
daily_difference = round(daily_difference, 2)
percent_variation = round(100 * daily_difference / stock_value_today, 2)

# Generate Arrow Direction
if stock_value_today > stock_value_yesterday:
    variation = '▲'
elif stock_value_today < stock_value_yesterday:
    variation = '▼'
else:
    variation = '▶'

print(f'{daily_difference}$')
print(f'Variation: {percent_variation}% {variation}')