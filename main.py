
import requests
import smtplib
import datetime as dt
import os
from dotenv import load_dotenv
load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_API=os.getenv("NEWS_API")
ALPHA_API=os.getenv("ALPHA_API")
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
MY_EMAIL=os.getenv("MY_EMAIL")
TO_EMAIL=os.getenv("TO_EMAIL")
E_PASS=os.getenv("E_PASS")
# today=dt.datetime.now()
# yesterday=today-dt.timedelta(days=1)
# yesterday_formatted=yesterday.strftime('%Y-%m-%d')

parameters_alpha={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":ALPHA_API
}

parameters_news={
    "apiKey":NEWS_API,
    "q":COMPANY_NAME,
    "searchIn":"title",
    "pageSize":3
    
}
response_alpha=requests.get(STOCK_ENDPOINT,params=parameters_alpha)
response_alpha.raise_for_status()
data_alpha=response_alpha.json()["Time Series (Daily)"]
data_alpha_dict={key:value["4. close"] for (key,value) in data_alpha.items()}
yesterday_stock=float(data_alpha_dict["2024-10-25"])


before_yesterday_stock=float(data_alpha_dict["2024-10-24"])
positive_difference=abs(yesterday_stock-before_yesterday_stock)
percentage_difference=(positive_difference/yesterday_stock)*100


if percentage_difference<5:

    response_news=requests.get(NEWS_ENDPOINT, params=parameters_news)
    response_news.raise_for_status()
    data_news=response_news.json()["articles"]


    list_three_articles=[f"Headline:{article['title']}\nBrief:{article['description']}" for article in data_news]

    for article in list_three_articles:
        with smtplib.SMTP("smtp.gmail.com",587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=E_PASS)
            message = f"Subject: Trading Message\n\n{article}".encode("utf-8")
            connection.sendmail(from_addr=MY_EMAIL,to_addrs=TO_EMAIL,msg=message)




