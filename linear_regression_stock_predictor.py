import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Fetch historical stock data
def get_stock_data(ticker, start='2020-01-01', end='2025-01-01'):
    stock_data = yf.download(ticker, start=start, end=end)
    return stock_data[['Close']]

# Prepare the dataset
def prepare_data(data, lookback=10):
    X, y = [], []
    for i in range(len(data) - lookback):
        X.append(data[i:i+lookback])
        y.append(data[i+lookback])
    return np.array(X), np.array(y)

# Load data
ticker = 'AAPL'  # Change this to any stock symbol
data = get_stock_data(ticker)
data = data.dropna()

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data)

# Prepare training and testing datasets
lookback = 10  # Number of past days to use as input
X, y = prepare_data(data_scaled.flatten(), lookback)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Rescale predictions back to original values
y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))
y_pred_inv = scaler.inverse_transform(y_pred.reshape(-1, 1))

# Evaluate the model
mae = mean_absolute_error(y_test_inv, y_pred_inv)
mse = mean_squared_error(y_test_inv, y_pred_inv)
print(f"MAE: {mae:.2f}, MSE: {mse:.2f}")

# Plot actual vs. predicted prices
plt.figure(figsize=(12, 6))
plt.plot(y_test_inv, label='Actual Price', color='blue')
plt.plot(y_pred_inv, label='Predicted Price', linestyle='dashed', color='red')
plt.xlabel('Days')
plt.ylabel('Stock Price')
plt.title(f'{ticker} Price Prediction using Linear Regression')
plt.legend()
plt.show()
