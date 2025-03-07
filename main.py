import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
import requests

def plot_history(ticker, period):
    stock = yf.download(ticker, period=period)

    if stock.empty:
        print("Error - No data found!")
        return

    plt.figure(figsize=(10,5))
    plt.plot(stock.index, stock['Close'],label=f"{ticker} Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Stock Price (USD)")
    plt.title(f"{ticker} Stock Price History for {period}")
    plt.legend()
    plt.grid()
    plt.show()

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
        period = input("ENTER A PERIOD (1mo, 2mo, 3mo...): ")
        break
    else:
        print(f"Invalid Stock Name - Try Again.")

plot_history(stock, period)

