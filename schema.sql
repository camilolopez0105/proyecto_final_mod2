-- Schema for Brazilian E-commerce Analysis
-- Run these queries in TiDB Cloud SQL Editor

CREATE DATABASE proyecto_final;

USE proyecto_final;

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

-- Analytical query (JOIN to create the analytical dataset)
SELECT
    o.order_id,
    o.order_date,
    o.order_status,
    c.customer_city,
    c.customer_state,
    oi.price,
    oi.freight_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered';