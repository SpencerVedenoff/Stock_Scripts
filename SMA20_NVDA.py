import backtrader as bt
import yfinance as yf
import pandas as pd
import datetime

# Step 1: Fetch NVDA data using yfinance
data = yf.download("NVDA", start="2020-01-01", end="2025-01-01")

# Rename columns to match Backtrader's expected format
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]  # Remove unwanted columns
data.columns = ['open', 'high', 'low', 'close', 'volume']  # Convert to lowercase
data['datetime'] = data.index  # Ensure there's a datetime column
data = data[['datetime', 'open', 'high', 'low', 'close', 'volume']]  # Reorder columns
data.set_index('datetime', inplace=True)  # Set index to datetime

# Step 2: Define Backtrader PandasData Feed
class PandasData(bt.feeds.PandasData):
    params = (
        ('datetime', None),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', None),  # Backtrader requires this, but it's not used
    )

# Step 3: Define Mean Reversion Strategy
class MeanReversionStrategy(bt.Strategy):
    params = (("period", 20), ("devfactor", 2))

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(period=self.params.period)
        self.std = bt.indicators.StandardDeviation(period=self.params.period)
        self.upper_band = self.sma + self.params.devfactor * self.std
        self.lower_band = self.sma - self.params.devfactor * self.std

    def next(self):
        if self.data.close[0] < self.lower_band[0]:  # Buy Signal (Oversold)
            self.buy()
        elif self.data.close[0] > self.upper_band[0]:  # Sell Signal (Overbought)
            self.sell()

# Step 4: Set up Backtrader Engine
cerebro = bt.Cerebro()
cerebro.addstrategy(MeanReversionStrategy)

# Load NVDA Data into Backtrader
data_feed = PandasData(dataname=data)
cerebro.adddata(data_feed)

# Run Backtest
cerebro.run()
cerebro.plot()

