import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance
from pymongo import MongoClient
import certifi


# ==============================  DB CONNECTION SETUP  ==============================
DB = "shif"
COLLECTION = "stocks"
MONGODB_URI = "INSERRT YOUR CONNECTION STRING HERE"

client = MongoClient(
    MONGODB_URI, tlsCAFile=certifi.where())

collection = client[DB][COLLECTION]

# ==================================================================================


# ==============================  GET STOCK DATA  =================================

def get_prices_history(from_day, to_day, symbol):

    print(f"Downloading data for {symbol} .....")
    yfinance.pdr_override()
    df = pdr.get_data_yahoo([symbol], from_day, to_day)

    prices = []
    # Manipulate the data to create a document representing the stock price
    for day in df.index:

        stock = {
            "symbol": symbol,
            "day": day,
            "price": round(df["Open"][day], 2)
        }

        prices.append(stock)

    return prices


# ==============================  MAIN  =================================
DAYS_OF_DATA = 3653  # These is to get the last 10 years of stock data

# Define dates interval
to_day = dt.datetime.now()
from_day = to_day - dt.timedelta(days=DAYS_OF_DATA)

# Lists of stocks to retrieve
# TOP 20 COMPANIES SYMBOL, UPDATED AT 4TH MARCH 2024, https://stockanalysis.com/list/biggest-companies/
top20_stocks_list_symbol = ["MSFT", "AAPL", "NVDA", "GOOGL", "META", "LLY", "TSM", "AVGO", "TSLA", "V", "NVO", "JPM", "WMT", "UNH",
                            "MA", "XOM", "ASML", "JNJ", "HD", "PG"]

other_stocks = ["COST", "TM", "AMD", "MRK", "ABBV", "ORCL", "CRM", "CVX", "BAC", "NFLX", "ADBE", "KO", "ACN", "PEP", "SAP", "FMX", "TMO", "LIN", "MCD", "NVS", "ABT", "DIS", "SHEL", "AZN", "CSCO", "WFC", "TMUS", "INTC", "DHR", "INTU", "QCOM", "BABA", "AMAT", "GE", "IBM", "CAT", "VZ", "PDD", "CMCSA", "AXP", "TXN",
                "UNP", "NKE", "NOW", "BX", "TTE", "AMGN", "HSBC", "MS", "BHP", "PFE", "ISRG", "LOW", "PM", "HDB", "RY", "SYK", "COP", "SPGI", "HON", "UPS", "LRCX", "GS", "PLD", "BLK", "MUFG", "UL", "BA", "T", "SCHW", "BUD", "BKNG", "RTX", "ETN", "SNY", "ELV", "MDT", "TJX", "NEE", "PGR", "VRTX", "PBR", "C", "TD", "SONY"]

stocks = []

for symbol in top20_stocks_list_symbol:

    stocks += get_prices_history(from_day, to_day, symbol)

# Insert stocks in the database
collection.insert_many(stocks)
