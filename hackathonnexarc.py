# -*- coding: utf-8 -*-
"""HackaThonNexarc.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZLXm0u0we5Jf-8ZuRHfaw9THKhRySbi7
"""

import pandas as pd
import numpy as np
import plotly.express as px
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
#importedLibs
# Reading the data from the Excel:
data = pd.read_csv("demand_inventory.csv")

print(data.columns)
print(data.head())

fig_demand = px.line(data, x='Date',
                     y='Demand',
                     title='Demand Over Time')
fig_demand.show()

fig_inventory = px.line(data, x='Date',
                        y='Inventory',
                        title='Inventory Over Time')
fig_inventory.show()

# Set index as date
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')
data = data.set_index('Date')

# Building model with optimized parameters
order = (1, 1, 1)
seasonal_order = (0, 1, 1, 7)
model = SARIMAX(data['Demand'], order=order, seasonal_order=seasonal_order)

# Fitting model
model_fit = model.fit()

# Making forecast
forecast = model_fit.forecast(steps=30)

# Printing demand_forecast
print(forecast)

#Inventory Optimization#

# Fitting SARIMAX model
model = SARIMAX(data['Demand'], order=(1,1,1), seasonal_order=(0,1,1,7))
model_fit = model.fit()

# Forecasting demand
forecast = model_fit.forecast(steps=30)

# Setting parameters
initial_inventory = 5500
lead_time = 7
service_level = 0.9
holding_cost = 1
stockout_cost = 5

# Inventory optimization
z = abs(np.percentile(forecast, 100 * (1 - service_level)))
order_qty = np.ceil(forecast.mean() + z).astype(int)
reorder_pt = forecast.mean() * lead_time + z
safety_stock = reorder_pt - forecast.mean() * lead_time

holding_cost = holding_cost * (initial_inventory + 0.5 * order_qty)
stockout_cost = stockout_cost * max(0, forecast.mean() * lead_time - initial_inventory)
total_cost = holding_cost + stockout_cost

print("Optimal Order Quantity:", order_qty)
print("Reorder Point:", reorder_pt)
print("Safety Stock:", safety_stock)
print("Total Cost:", total_cost)

