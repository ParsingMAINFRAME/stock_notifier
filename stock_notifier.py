from stock_data import get_stock_price
from email_alert import send_email

ticker_symbol = "AAPL"
target_price = 150.00  # Set your price target

price = get_stock_price(ticker_symbol)

if price <= target_price:
    print(f"{ticker_symbol} has hit the target price of ${target_price}!")
    subject = f"{ticker_symbol} has hit the target price!"
    body = f"The current price of {ticker_symbol} is ${price}. This is at or below your target of ${target_price}."
    send_email(subject, body, "recipient_email@example.com")
else:
    print(f"{ticker_symbol} is still above the target price.")