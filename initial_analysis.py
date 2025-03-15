import pandas as pd

# Create DataFrames for each dataset
df_customers = pd.read_csv('data/raw/customers_data.csv')
df_products = pd.read_csv('data/raw/products_data.csv')
df_sales= pd.read_csv('data/raw/sales_data.csv')

# Most common customer location
most_common_region = df_customers['Region'].mode()[0]

# Highest/lowest product price
max_product_price = df_products['UnitPrice'].max()
min_product_price = df_products['UnitPrice'].min()

# Estimate average, minimum, maximum sales
avg_sales = round(df_sales['SaleAmount'].mean(), 2)
min_sales = df_sales['SaleAmount'].min()
max_sales = df_sales['SaleAmount'].max()

# Print statements with results
print(f"The most common region is: {most_common_region}")
print(f"The maximum product price is: {max_product_price}")
print(f"The minimum product price is: {min_product_price}")
print(f"The average sales amount is: {avg_sales}")
print(f"The minimum sales amount is: {min_sales}")
print(f"The maximum sales amount is: {max_sales}")

# There appears to be no issues with the data
