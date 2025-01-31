import yfinance as yf
import time

# Define stock symbol
STOCK_SYMBOL = "NVDA"

# Trading parameters
SMA_PERIOD = 20  # 20-day moving average
STD_FACTOR = 2   # Standard deviation multiplier

def get_trading_signal():
    # Fetch NVDA last 20 days of data
    stock_data = yf.download(STOCK_SYMBOL, period="1mo", interval="1d")

    # Ensure we have enough data
    if len(stock_data) < SMA_PERIOD:
        print("⚠️ Not enough data to calculate SMA. Waiting for more data.")
        return

    # Calculate 20-day SMA & standard deviation (convert to float)
    sma_20 = float(stock_data["Close"].rolling(window=SMA_PERIOD).mean().iloc[-1])
    std_20 = float(stock_data["Close"].rolling(window=SMA_PERIOD).std().iloc[-1])

    # Calculate Bollinger Bands
    upper_band = sma_20 + (STD_FACTOR * std_20)
    lower_band = sma_20 - (STD_FACTOR * std_20)

    # Get latest closing price (Ensure it's a float)
    latest_price = float(stock_data["Close"].iloc[-1])

    # Print the values
    print(f"\n🔹 NVDA Trading Update 🔹")
    print(f"Latest Price: ${latest_price:.2f}")
    print(f"20-Day SMA: ${sma_20:.2f}")
    print(f"Upper Band (Sell Zone): ${upper_band:.2f}")
    print(f"Lower Band (Buy Zone): ${lower_band:.2f}")

    # Determine trading signal
    if latest_price < lower_band:
        print("✅ BUY SIGNAL: Price is oversold!")
    elif latest_price > upper_band:
        print("❌ SELL SIGNAL: Price is overbought!")
    else:
        print("🔸 HOLD: Price is within normal range.")

# Run the script
if __name__ == "__main__":
    while True:
        get_trading_signal()
        time.sleep(86400)  # Check once per day
