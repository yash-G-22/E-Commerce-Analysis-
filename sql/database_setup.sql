-- Database Setup for Business Analytics Project
-- This script sets up the database structure for the Brazilian E-Commerce dataset

-- Create database (adjust name as needed)
CREATE DATABASE IF NOT EXISTS business_analytics;
USE business_analytics;

-- Create tables based on the dataset structure
-- Note: Adjust data types and constraints based on your specific database system

-- Orders table
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(20),
    order_purchase_date DATETIME,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME,
    INDEX idx_customer_id (customer_id),
    INDEX idx_purchase_date (order_purchase_date)
);

-- Customers table
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix VARCHAR(10),
    customer_city VARCHAR(50),
    customer_state VARCHAR(5)
);

-- Products table
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT,
    INDEX idx_category (product_category_name)
);

-- Order items table
CREATE TABLE order_items (
    order_id VARCHAR(50),
    order_item_id INT,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date DATETIME,
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2),
    PRIMARY KEY (order_id, order_item_id),
    INDEX idx_product (product_id)
);

-- Payments table
CREATE TABLE order_payments (
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(20),
    payment_installments INT,
    payment_value DECIMAL(10,2),
    PRIMARY KEY (order_id, payment_sequential),
    INDEX idx_payment_type (payment_type)
);

-- Reviews table
CREATE TABLE order_reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME,
    INDEX idx_order (order_id),
    INDEX idx_score (review_score)
);

-- Create foreign key relationships
ALTER TABLE orders ADD CONSTRAINT fk_orders_customer 
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

ALTER TABLE order_items ADD CONSTRAINT fk_items_order 
    FOREIGN KEY (order_id) REFERENCES orders(order_id);

ALTER TABLE order_items ADD CONSTRAINT fk_items_product 
    FOREIGN KEY (product_id) REFERENCES products(product_id);

ALTER TABLE order_payments ADD CONSTRAINT fk_payments_order 
    FOREIGN KEY (order_id) REFERENCES orders(order_id);

ALTER TABLE order_reviews ADD CONSTRAINT fk_reviews_order 
    FOREIGN KEY (order_id) REFERENCES orders(order_id);

-- Insert sample data (if needed for testing)
-- INSERT INTO customers VALUES ('customer_001', 'unique_001', '10000', 'São Paulo', 'SP');
-- INSERT INTO products VALUES ('product_001', 'electronics', 20, 100, 3, 500, 30, 20, 15);

print("Database setup completed successfully!");
