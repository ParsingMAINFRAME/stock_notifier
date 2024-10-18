import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy as np


def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")
    
    # Calculate 50-day and 200-day Simple Moving Averages (SMA)
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    
    # Calculate Relative Strength Index (RSI)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def plot_stock_data(df, ticker):
    plt.figure(figsize=(12,8))
    
    # Price and SMAs
    plt.subplot(2, 1, 1)
    plt.plot(df['Close'], label='Stock Price', color='blue')
    plt.plot(df['SMA_50'], label='50-Day SMA', color='green')
    plt.plot(df['SMA_200'], label='200-Day SMA', color='red')
    plt.title(f"{ticker} Stock Price and Moving Averages")
    plt.legend()

    # RSI
    plt.subplot(2, 1, 2)
    plt.plot(df['RSI'], label='RSI', color='purple')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red')  # Overbought line
    plt.axhline(30, linestyle='--', alpha=0.5, color='green')  # Oversold line
    plt.title(f"{ticker} Relative Strength Index (RSI)")
    plt.legend()

    plt.tight_layout()
    plt.show()

def send_email_alert(ticker, message):
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver_email@gmail.com"
    password = "your_password"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Stock Alert: {ticker}"
    
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_conditions(df, ticker):
    # Example condition: if price crosses 50-day SMA or RSI crosses 70 (overbought)
    last_row = df.iloc[-1]
    
    if last_row['Close'] > last_row['SMA_50']:
        message = f"{ticker} price crossed above 50-day SMA."
        send_email_alert(ticker, message)
    
    if last_row['RSI'] > 70:
        message = f"{ticker} is overbought with RSI of {last_row['RSI']}."
        send_email_alert(ticker, message)

def backtest_strategy(df):
    df['Signal'] = 0  # Initialize the Signal column
    df['Signal'][50:] = np.where(df['SMA_50'][50:] > df['SMA_200'][50:], 1, 0)  # Buy signal when 50-day SMA > 200-day SMA

    # Backtesting returns
    df['Position'] = df['Signal'].shift()  # Shift the signal column by 1 to get positions for the next day
    df['Strategy_Returns'] = df['Position'] * df['Close'].pct_change()

    total_return = df['Strategy_Returns'].sum()
    print(f"Total return from strategy: {total_return * 100:.2f}%")

if __name__ == "__main__":
    ticker = "AAPL"  # Replace with any stock ticker
    df = fetch_stock_data(ticker)
    
    plot_stock_data(df, ticker)
    check_conditions(df, ticker)
    backtest_strategy(df)