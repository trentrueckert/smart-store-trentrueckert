# smart-sales-starter-files

Starter files to initialize the smart sales project.

-----

## Project Setup Guide (Windows)

Run all commands from a PowerShell terminal in the root project folder.

### Step 2A - Create a Local Project Virtual Environment

```shell
py -m venv .venv
```

### Step 2B - Activate the Virtual Environment

```shell
.venv\Scripts\activate
```

### Step 2C - Install Packages

```shell
py -m pip install --upgrade -r requirements.txt
```

### Step 2D - Optional: Verify .venv Setup

```shell
py -m datafun_venv_checker.venv_checker
```

### Step 2E - Run the initial project script

```shell
py scripts/data_prep.py
```

-----

## Initial Package List

- pip
- loguru
- ipykernel
- jupyterlab
- numpy
- pandas
- matplotlib
- seaborn
- plotly
- pyspark==4.0.0.dev1
- pyspark[sql]
- git+https://github.com/denisecase/datafun-venv-checker.git#egg=datafun_venv_checker

-----

## Project 3

### Add Additional Data
1. Add additional columns:
   1. Customers - LastActiveYear, PreferredContactMethod
   2. Products - StockQuantity, StoreSection
   3. Sales - DiscountPercent, PaymentType
2. Load new data to the original raw file

### Clean and Prepare the Data
1. Create data prep scripts
   1. Create a subfolder 'data_preparation' in 'scripts'
   2. Create files in this subfolder for each raw file
2. Store the files in 'prepared' with new custom names
   1. 'customers_data_prepared.csv'
   2. 'products_data_prepared.csv'
   3. 'sales_data_prepared.csv'

```
py scripts/data_preparation/prepare_customers_data.py
py scripts/data_preparation/prepare_products_data.py
py scripts/data_preparation/prepare_sales_data.py
```

### Create Basic Data Scrubber
- The data is clean, but this will be more useful later
1. Create 'data_scrubber.py' in the 'scripts' folder
2. Create 'tests' folder with 'test_data_scrubber.py'
3. Run 'test_data_scrubber.py' to ensure it works

```
py tests/test_data_scrubber.py
```

-----

## Project 4

### Design Data Warehouse
- Choose the best schema design for the warehouse (we use star schema for this project)
- Plan out the schema to show the structure of the database

### Create the Data Warehouse
- In the scripts folder, create the file etl_to_dw.py
- Optional: Create a separate SQL file to verify/test the create_table statements
- In the etl_to_dw.py file, copy and paste the code from the example repo and make the adjustments needed for the specific added columns from the prepared data

### Run the Script to Create the Warehouse
- The command for Windows:

```
py scripts/etl_to_dw.py
```

## Project 5
1. Describe your SQL queries and reports:
   1. We use various charts and graphs to show trends in our datasets with the SQL queries and reports detailed from our instructions
   2. Slicer for sale date range
   3. A matrix for total sale amount by category and region
   4. A clustered column chart for total sale amount by year, quarter, month
   5. A line chart for sales trends
   6. A bar chart for Top Customers
   7. A slicer for category
   8. A slicer for region
2. Explain dashboard design choices:
   1. I tried to keep the slicers towards the outside and the visualizations more to the middle
3. Include screenshot of Power BI Model View / Spark SQL Schema: ![Power BI Model View](C:\Users\trent\OneDrive\Pictures\Screenshots 1\PowerBIModelView.png)
4. Include screenshot of Query results: ![Query Results](C:\Users\trent\OneDrive\Pictures\Screenshots 1\QueriesP5.png)
5. Include screenshot of Final Dashboard / Charts: ![Final Dashboard](C:\Users\trent\OneDrive\Pictures\Screenshots 1\DashboardP5.png)