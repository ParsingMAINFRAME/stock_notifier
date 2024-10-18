import yfinance as yf

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.history(period="1d")
    current_price = stock_info['Close'][0]
    return current_price