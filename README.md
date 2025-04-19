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

-----

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
3. Include screenshot of Power BI Model View / Spark SQL Schema: ![Power BI Model View](images/PowerBIModelView.png)
4. Include screenshot of Query results: ![Query Results](images/QueriesP5.png)
5. Include screenshot of Final Dashboard / Charts: ![Final Dashboard](images/DashboardP5.png)

-----

## Project 6
### Section 1: The Business Goal
* The business goal here is to analyze the sales trends by region and year/month to see which products sell the best, and to decide whether to increase or decrease the number of each product based on the results. If products are not selling in certain regions or certain times of the year, the business could do further analysis on why to see if it is worth it to keep supplying the same amount of products, and vice versa for if they are selling well.

### Section 2: Data Source
* I used olap_cubing.py to generate an OLAP cube from sales data stored in my SQLite database (smart_sales.db).
* From the sale table, I used: Year and Month (extracted from sale_date), sale_amount_sum (changed to total_sales), and sale_id_count.
* From the product table, I used: product_name.
* From the customer table. I used: region.

### Section 3: Tools
* I used some of the framework from (https://github.com/denisecase/smart-sales-olap/blob/main/scripts/olap_cubing.py) for my olap_cubing.py file.
* I used some of the framework from (https://github.com/denisecase/smart-sales-olap/blob/main/scripts/olap_goal_top_product_by_day.py) as well to get going on my olap_goal files.
* ChatGPT was utilized a bit to iron out any kinks in the olap_goal files.

### Section 4: Workflow & Logic
#### Dimensions
* The dimensions I used were Year, Month, region, and product_name.

#### Aggregations
* For total sales, I used the sum of sales and grouped it by Year, Month, region, and product_name.
* For the number of sales, I used the count of sales_id and grouped it by the the same as above. 

#### Logic
* To calculate the top products by month and region, I grouped the total sales by month and region and took a head of the top 3 products per month per region. The bar chart depicts these well.
* To calculate the top product volumn by region, I took the same approach but also grouped month and year together to showed a drilled-down heatmap, as well as a bar chart. 

### Section 5-6: Results and Suggested Business Action
* The results of the top products by total sales show not extremely surprising results, with laptops leading in 3 of 4 regions. This is to be expected as they are the most expensive product from the data. Overall, there is not much spending across all of the regions, and particularly so in the North. 
* The results of the top products by sale counts bar chart is fairly sporadic with not many noticeable trends except for one that stood out to me: jacket purchases in August. This makes sense because in most of the represented regions, it tends to get colder just after August. 
* The heatmap for top products by sale counts is the best overall visual in my opinion. It gives great detail on which months and regions are the most products are purchased in, with the East far and away having the most. I find it interesting that there were hardly any in October. I wish there were some in November or December, as analyzing Christmas purchasing could be huge.
* I would recommend further research on why the North wasn't purchasing much at all, and for data that includes November and December.

![Top Products Total Sales by Month and Region](data/results/top_products_by_region_month.png)

![Top Products Sale Amounts by Month and Region Bar Chart](data/results/top_products_by_sales_counts_month.png)

![Top Products Sale Amounts by Month and Region Heatmap](data/results/sales_heatmap_region_year.png)

### Section 7: Challenges
* I had some challenges with getting the graphs to be able to present how I wanted.
  * ChatGPT helped me fix a couple of minor errors.
* I had an issue getting my scripts to run at first.
  * I changed the format of the command I was using and had no further issues.