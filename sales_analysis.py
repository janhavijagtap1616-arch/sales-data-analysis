# -----------------------------------------------
# SALES ANALYSIS SCRIPT (CLEAN & UPDATED VERSION)
# -----------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# Step 1: Load Sales Data
# -----------------------------
file_csv = "sales_data_expanded.csv"
file_xlsx = "sales_data_expanded.xlsx"

if os.path.exists(file_csv):
    data = pd.read_csv(file_csv)
    print(f"Loaded data from {file_csv}")
elif os.path.exists(file_xlsx):
    data = pd.read_excel(file_xlsx)
    print(f"Loaded data from {file_xlsx}")
else:
    raise FileNotFoundError("No sales_data.csv or sales_data_expanded.xlsx file found!")

print("\nInitial Data:\n", data.head())

# -----------------------------
# Step 2: Data Cleaning
# -----------------------------
# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Check for missing values
print("\nMissing Values:\n", data.isnull().sum())

# Fill missing Quantity or Price with median (fixed future warning)
data.fillna({
    'Quantity': data['Quantity'].median(),
    'Price': data['Price'].median()
}, inplace=True)

# Drop rows with missing Date or Product/Region
data.dropna(subset=['Date', 'Product', 'Region'], inplace=True)

# -----------------------------
# Step 3: Add Calculated Columns
# -----------------------------
# Total Sales per row
data['Total_Sales'] = data['Quantity'] * data['Price']

# Average price per product
avg_price = data.groupby('Product')['Price'].mean()
print("\nAverage Price per Product:\n", avg_price)

# Month and Year columns
data['Month'] = data['Date'].dt.month
data['Year'] = data['Date'].dt.year

# -----------------------------
# Step 4: Sales Analysis
# -----------------------------
# 1. Total sales by Product
sales_by_product = data.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
print("\nTotal Sales by Product:\n", sales_by_product)

# 2. Total sales by Region
sales_by_region = data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False)
print("\nTotal Sales by Region:\n", sales_by_region)

# 3. Top 3 Products
top_products = sales_by_product.head(3)
print("\nTop 3 Products:\n", top_products)

# 4. Monthly Sales Trend
monthly_sales = data.groupby('Month')['Total_Sales'].sum()
print("\nMonthly Sales:\n", monthly_sales)

# 5. Region-wise Product Sales
region_product_sales = data.groupby(['Region', 'Product'])['Total_Sales'].sum().unstack()
print("\nRegion-wise Product Sales:\n", region_product_sales)

# -----------------------------
# Step 5: Visualization
# -----------------------------
# ✅ FIXED STYLE ISSUE — use updated seaborn style
plt.style.use('seaborn-v0_8-darkgrid')

# Bar chart: Total Sales by Product
plt.figure(figsize=(8,5))
sales_by_product.plot(kind='bar', color='skyblue')
plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.show()

# Pie chart: Sales by Region
plt.figure(figsize=(6,6))
sales_by_region.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title("Sales by Region")
plt.ylabel('')
plt.tight_layout()
plt.show()

# Line chart: Monthly Sales Trend
plt.figure(figsize=(8,5))
monthly_sales.plot(kind='line', marker='o', color='green')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(monthly_sales.index)
plt.tight_layout()
plt.show()

# Heatmap: Region-wise Product Sales
plt.figure(figsize=(10,5))
sns.heatmap(region_product_sales, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Region-wise Product Sales")
plt.tight_layout()
plt.show()

# Combined Plot: Bar + Line
fig, ax1 = plt.subplots(figsize=(8,5))
ax1.bar(sales_by_product.index, sales_by_product.values, color='lightcoral', label='Total Sales')
ax1.set_xlabel("Product")
ax1.set_ylabel("Total Sales")
ax2 = ax1.twinx()
ax2.plot(sales_by_product.index, avg_price[sales_by_product.index], color='blue', marker='o', label='Average Price')
ax2.set_ylabel("Average Price")
plt.title("Product Sales vs Average Price")
fig.legend(loc="upper right", bbox_to_anchor=(1,1))
plt.tight_layout()
plt.show()

# -----------------------------
# Step 6: Export Cleaned Data and Analysis
# -----------------------------
data.to_csv("cleaned_sales_data.csv", index=False)
sales_by_product.to_csv("sales_by_product.csv")
sales_by_region.to_csv("sales_by_region.csv")
monthly_sales.to_csv("monthly_sales.csv")

print("\n✅ Data cleaned, analyzed, visualized, and exported successfully!")
