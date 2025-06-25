-- Create the database
CREATE DATABASE IF NOT EXISTS talk2db;
USE talk2db;

-- User Authentication Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NULL,
    password_hash VARCHAR(255) NOT NULL,  -- Hashed password storage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products Table (Stores details of products)
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sales Table (Stores real-time sales data)
CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity_sold INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

-- Query Logs Table (Stores user queries and their SQL translation)
CREATE TABLE query_logs (
    query_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    user_question TEXT NOT NULL,
    generated_sql TEXT NOT NULL,
    query_result TEXT,  -- Stores JSON/text results
    query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
-- Insert Sample Users
INSERT INTO users (username, email, password_hash) 
VALUES 
('karthika', 'karthikap858@gmail.com', 'hashed_password1'),
('harshini', 'harshini@example.com', 'hashed_password2'),
('alice_wonder', 'alice@example.com', 'hashed_password3'),
('michael_smith', 'michael@example.com', 'hashed_password4'),
('emma_jones', 'emma@example.com', 'hashed_password5'),
('david_wilson', 'david@example.com', 'hashed_password6'),
('olivia_brown', 'olivia@example.com', 'hashed_password7');


-- Insert Sample Products
INSERT INTO products (product_name, category, price, stock_quantity) 
VALUES 
('Laptop', 'Electronics', 75000, 20),
('Smartphone', 'Electronics', 50000, 50),
('Office Chair', 'Furniture', 12000, 15),
('Gaming Laptop', 'Electronics', 120000, 10),
('Bluetooth Headphones', 'Electronics', 4000, 50),
('Wireless Mouse', 'Electronics', 1200, 75),
('Office Desk', 'Furniture', 18000, 8),
('LED Monitor', 'Electronics', 15000, 20),
('Smartwatch', 'Electronics', 10000, 35),
('Ergonomic Chair', 'Furniture', 15000, 12),
('Tablet', 'Electronics', 30000, 25),
('Coffee Table', 'Furniture', 8000, 15),
('Printer', 'Electronics', 18000, 18);

-- Insert Sample Sales
INSERT INTO sales (user_id, product_id, quantity_sold, total_price) 
VALUES 
(1, 1, 1, 75000),
(2, 2, 2, 100000),
(1, 3, 1, 12000),
(2, 5, 1, 15000), 
(3, 8, 2, 60000), 
(4, 1, 1, 120000),
(5, 6, 1, 10000), 
(1, 7, 1, 15000), 
(3, 9, 2, 16000), 
(4, 2, 1, 4000), 
(2, 10, 1, 18000), 
(5, 3, 3, 3600), 
(1, 4, 1, 18000); 

INSERT INTO query_logs (user_id, user_question, generated_sql, query_result)
VALUES 
(1, 'Show me all electronics products.', 
    'SELECT * FROM products WHERE category = "Electronics";', 
    '[{"product_name": "Laptop", "price": 75000}, {"product_name": "Smartphone", "price": 50000}]'),

(2, 'What is the total sales revenue?', 
    'SELECT SUM(total_price) AS revenue FROM sales;', 
    '[{"revenue": 431600}]'),

(3, 'Who bought the most expensive product?', 
    'SELECT u.username, p.product_name, s.total_price FROM sales s JOIN users u ON s.user_id = u.user_id JOIN products p ON s.product_id = p.product_id ORDER BY s.total_price DESC LIMIT 1;', 
    '[{"username": "Michael_smith", "product_name": "Gaming Laptop", "total_price": 120000}]'),

(4, 'What are the top-selling products?', 
    'SELECT p.product_name, SUM(s.quantity_sold) AS total_sold FROM sales s JOIN products p ON s.product_id = p.product_id GROUP BY p.product_name ORDER BY total_sold DESC;', 
    '[{"product_name": "Tablet", "total_sold": 2}, {"product_name": "Coffee Table", "total_sold": 2}]'),

(5, 'How many users have made purchases?', 
    'SELECT COUNT(DISTINCT user_id) AS active_users FROM sales;', 
    '[{"active_users": 5}]');

ALTER TABLE users MODIFY COLUMN email VARCHAR(255) NULL;

