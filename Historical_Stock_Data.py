import yfinance as yf

# Download historical stock data for Tesla (TSLA)
stock = yf.download("TSLA", start="2020-01-01", end="2024-01-01")
# Download historical stock data for Apple (AAPL)
stock2 = yf.download("AAPL", start="2020-01-01", end="2024-01-01")

# Display the first few rows
print(stock.head())
print(stock2.head())

