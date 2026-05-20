# Brazilian E-commerce Analysis Dashboard

End-to-end data project analyzing the Brazilian Olist E-commerce dataset (2016-2018). From CSV files to a cloud database (TiDB), through ETL, EDA, and an interactive Streamlit dashboard.

## Project Flow

```
CSV (Kaggle) → TiDB Cloud → Python (ETL + EDA) → Streamlit Dashboard
```

## Project Structure

```
proyecto_final_mod2/
├── app.py                         # Streamlit dashboard
├── credenciales.py                # TiDB connection credentials (NOT committed)
├── dataset_analitico.pkl          # Analytical dataset (generated)
├── olist_customers_dataset.csv    # Kaggle dataset - customers
├── olist_orders_dataset.csv       # Kaggle dataset - orders
├── olist_order_items_dataset.csv  # Kaggle dataset - order items
├── proyecto_final_modulo2.ipynb   # ETL + EDA notebook
├── requirements.txt               # Python dependencies
└── README.md
```

## Technologies

- **Database**: TiDB Cloud (MySQL-compatible, Serverless tier)
- **Libraries**: pandas, mysql-connector-python, matplotlib
- **Dashboard**: Streamlit

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure credentials

Create a `credenciales.py` file (never commit this file):

```python
mysql_config = {
    "host": "your-host.gateway.tidbcloud.com",
    "port": 4000,
    "user": "your-user.root",
    "password": "your-password",
    "database": "proyecto_final",
    "ssl_disabled": False,
}
```

### 3. Database setup

1. Create a free cluster at [TiDB Cloud](https://tidbcloud.com)
2. Create the `proyecto_final` database:
   ```sql
   CREATE DATABASE proyecto_final;
   ```

3. Create tables:
   ```sql
   CREATE TABLE customers (
       customer_id VARCHAR(50) PRIMARY KEY,
       customer_city VARCHAR(100),
       customer_state VARCHAR(5)
   );

   CREATE TABLE orders (
       order_id VARCHAR(50) PRIMARY KEY,
       customer_id VARCHAR(50),
       order_status VARCHAR(20),
       order_date DATETIME,
       FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
   );

   CREATE TABLE order_items (
       order_item_id INT PRIMARY KEY,
       order_id VARCHAR(50),
       product_id VARCHAR(50),
       seller_id VARCHAR(50),
       price DECIMAL(10,2),
       freight_value DECIMAL(10,2),
       FOREIGN KEY (order_id) REFERENCES orders(order_id)
   );
   ```

## Running the Dashboard

```bash
streamlit run app.py
```

The dashboard includes:
- State filter (sidebar)
- Key metrics (orders, sales, revenue, freight)
- Top 20 cities by sales and orders
- Temporal analysis (monthly/yearly trends)
- Analytical conclusions

## Key Findings

- **São Paulo (SP)** dominates with 42% of total sales (~R$ 4.6M) and 42% of all orders
- **São Paulo city** alone generates R$ 1.68M in sales (~14% of total revenue)
- **Freight costs** add approximately 10% to total order value
- Dataset spans 2016-2018, showing steady e-commerce growth in Brazil

## Dataset Source

[Kaggle - Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)