import numpy as np
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Fetch historical stock data
def get_stock_data(ticker, start='2020-01-01', end='2025-01-01'):
    stock_data = yf.download(ticker, start=start, end=end)
    if stock_data.empty:
        raise ValueError(f"Error: No data found for {ticker}. Check the ticker symbol and date range.")
    return stock_data[['Close']]  # Return as DataFrame

# Define stock pair
ticker1 = 'SPY'  # Example stock 1
ticker2 = 'QQQ'  # Example stock 2

# Fetch data
data1 = get_stock_data(ticker1)
data2 = get_stock_data(ticker2)

# Debugging: Check downloaded data
print(f"Data type of {ticker1}: {type(data1)}")
print(f"Data type of {ticker2}: {type(data2)}")
print(f"First rows of {ticker1}:\n{data1.head()}")
print(f"First rows of {ticker2}:\n{data2.head()}")

# Ensure both datasets align properly by merging on the index
data = data1.join(data2, how='inner', lsuffix=f'_{ticker1}', rsuffix=f'_{ticker2}')
data.columns = [ticker1, ticker2]  # Rename columns properly
data = data.dropna()  # Remove any missing values

print(data.info())  # Check for NaN values and alignment issues

# Perform linear regression to find hedge ratio
X = sm.add_constant(data[ticker2])
y = data[ticker1]
model = sm.OLS(y, X).fit()
hedge_ratio = model.params[1]
print(f"Hedge Ratio: {hedge_ratio:.2f}")

# Calculate spread
spread = data[ticker1] - hedge_ratio * data[ticker2]
mean_spread = spread.mean()
std_spread = spread.std()

# Generate trading signals
buy_signal = spread < (mean_spread - 1.5 * std_spread)
sell_signal = spread > (mean_spread + 1.5 * std_spread)

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(spread, label='Spread', color='blue')
plt.axhline(mean_spread, color='black', linestyle='dashed', label='Mean')
plt.axhline(mean_spread + 1.5 * std_spread, color='red', linestyle='dashed', label='+1.5 Std Dev')
plt.axhline(mean_spread - 1.5 * std_spread, color='green', linestyle='dashed', label='-1.5 Std Dev')
plt.scatter(spread.index[buy_signal], spread[buy_signal], color='green', marker='^', label='Buy Signal')
plt.scatter(spread.index[sell_signal], spread[sell_signal], color='red', marker='v', label='Sell Signal')
plt.xlabel('Date')
plt.ylabel('Spread Value')
plt.title(f'Pairs Trading Strategy: {ticker1} vs {ticker2}')
plt.legend()
plt.show()
