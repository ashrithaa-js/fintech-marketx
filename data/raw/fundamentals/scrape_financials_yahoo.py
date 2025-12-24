import yfinance as yf
import pandas as pd

def get_financials(symbol):
    stock = yf.Ticker(symbol)

    income = stock.financials.T
    balance = stock.balance_sheet.T
    cashflow = stock.cashflow.T

    income.to_csv(f"data/raw/fundamentals/{symbol}_income.csv")
    balance.to_csv(f"data/raw/fundamentals/{symbol}_balance.csv")
    cashflow.to_csv(f"data/raw/fundamentals/{symbol}_cashflow.csv")

get_financials("AAPL")
