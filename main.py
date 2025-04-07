import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def process(ticker):

    end_date = datetime.today() - timedelta(days=1)
    end_str = end_date.strftime('%Y-%m-%d')
    df = yf.download(ticker, start="2020-01-01", end=end_str)

    df['Target'] = df['Close'].shift(-1) > df['Close'] # if true, then the stock price rose, else falsae
    df['Target'] = df['Target'].astype(int) # true = 1 = stock price rose, false = 0 = stock price fell
    df.dropna(inplace=True)

    df['Return'] = df['Close'].pct_change() #calculate the percentage change between the previous and current closing prices
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['MA_10'] = df['Close'].rolling(window=10).mean()
    df['RollingMean_7'] = df['Close'].rolling(7).std()

    features = ['Return', 'MA_7', 'MA_10', 'RollingMean_7']
    x = df[features]
    y = df['Target']

    split_val = int(len(df) * 0.8)
    X_train, X_test = x[:split_val], x[split_val:]
    Y_train, Y_test = y[:split_val], y[split_val:]

    clf = RandomForestClassifier()
    clf.fit(X_train, Y_train)
    prediction = clf.predict(X_test)

    accuracy = accuracy_score(Y_test, prediction)
    print(f'Accuracy Score: {accuracy:.2f}')


list_of_stocks = {}

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", {"id": "constituents"})

for row in table.find_all("tr")[1:]: #finds all table rows <tr> within the table
    columns = row.find_all("td")
    if len(columns) > 1:
        ticker = columns[0].text.strip()
        company = columns[1].text.strip()
        list_of_stocks[ticker] = company

stock = None
period = None
while True:
    stock = input("ENTER THE STOCK OR TYPE 'LIST' TO GET A LIST: ")
    if(stock == 'LIST'):
        for stock, name in list_of_stocks.items():
            print(f"{stock}: {name}")
        print()
        continue

    if stock in list_of_stocks:
        break
    else:
        print(f"Invalid Stock Name - Try Again.")

process(stock)

