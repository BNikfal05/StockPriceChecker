import requests
from twilio.rest import Client

STOCK_NAME = "NVDA"
COMPANY_NAME = "NVIDIA Corporation"
NEWS_API_KEY = "YOUR KEY"
NEWS_ENDPOINT = 'https://newsapi.org/v2/everything'
STOCK_API_KEY = "YOUR KEY"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
TWILIO_SID = "YOUR SID"
TWILIO_AUTH_TOKEN = "YOUR AUTH TOKEN"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

# Stock API
response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
diff_percent = round(100 * (difference / float(yesterday_closing_price)), 2)

up_down = '▲' if difference > 0 else '▼'

if abs(diff_percent) > 0:
    # News API
    news_params = {
        'apiKey': NEWS_API_KEY,
        'qInTitle': COMPANY_NAME
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    # Twilio API
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+TWILIO PHONE',
            to='+YOUR PHONE'
        )
print('done')