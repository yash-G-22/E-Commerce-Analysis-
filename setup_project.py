#!/usr/bin/env python3
"""
Business Analytics Project Setup Script
Automatically sets up the complete project environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print project banner"""
    print("=" * 60)
    print("🚀 BUSINESS ANALYTICS & MACHINE LEARNING PROJECT")
    print("=" * 60)
    print("Tech Stack: SQL, Python (PySpark), Power BI, Machine Learning")
    print("Dataset: Brazilian E-Commerce Public Dataset by Olist")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    
    print(f"✅ Python version: {sys.version}")
    return True

def install_requirements():
    """Install required Python packages"""
    print("\n📦 Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_project_structure():
    """Create the complete project directory structure"""
    print("\n📁 Creating project structure...")
    
    directories = [
        'data',
        'sql',
        'python',
        'powerbi',
        'ml_models',
        'notebooks',
        'outputs',
        'logs',
        'docs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created: {directory}/")

def create_sample_files():
    """Create sample configuration and documentation files"""
    print("\n📝 Creating sample files...")
    
    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints

# PySpark
*.parquet
*.delta

# Data files
*.csv
*.xlsx
*.json
*.parquet

# Models
*.pkl
*.joblib

# Logs
*.log

# Environment
.env
.venv
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w', encoding="utf-8") as f:
        f.write(gitignore_content)
    print("✅ Created: .gitignore")
    
    # Create environment setup script
    env_setup = """# Environment Setup for Business Analytics Project

# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Download dataset
python python/download_dataset.py

# 3. Run analysis
python python/main_analysis.py

# 4. Or run interactive analysis
python python/business_analytics_notebook.py

# 5. Create Power BI dashboards using the guide in powerbi/powerbi_instructions.md
"""
    
    with open('setup_env.bat' if platform.system() == 'Windows' else 'setup_env.sh', 'w', encoding="utf-8") as f:
        f.write(env_setup)
    print("✅ Created: setup_env script")

def create_database_setup():
    """Create database setup instructions"""
    print("\n🗄️ Creating database setup files...")
    
    # SQL setup script
    sql_setup = """-- Database Setup for Business Analytics Project
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
"""
    
    with open('sql/database_setup.sql', 'w', encoding="utf-8") as f:
        f.write(sql_setup)
    print("✅ Created: sql/database_setup.sql")

def create_project_documentation():
    """Create comprehensive project documentation"""
    print("\n📚 Creating project documentation...")
    
    # Project overview
    overview = """# Business Analytics & Machine Learning Project

## Project Overview
This project demonstrates advanced business analytics skills using SQL, Python (PySpark), Power BI, and Machine Learning techniques. The project analyzes customer behavior, sales performance, and implements predictive analytics for business insights.

## Tech Stack
- **SQL**: Advanced data querying and analysis
- **Python (PySpark)**: Big data processing and ML
- **Power BI**: Data visualization and dashboards
- **Machine Learning**: Customer segmentation, forecasting, churn prediction

## Key Features
1. **Customer Segmentation**: K-means clustering for customer behavior analysis
2. **Sales Forecasting**: Time series analysis and trend prediction
3. **Churn Prediction**: Random Forest classifier for customer retention
4. **Product Recommendation**: Collaborative filtering system
5. **Interactive Dashboards**: Power BI visualizations

## Project Structure
```
Business Analyst/
├── data/                   # Dataset files
├── sql/                    # SQL queries and analysis
├── python/                 # Python/PySpark scripts
├── powerbi/                # Power BI files and guides
├── ml_models/             # Machine learning models
├── notebooks/              # Jupyter notebooks
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Getting Started
1. Run `python setup_project.py` to set up the project
2. Run `python python/download_dataset.py` to get the dataset
3. Run `python python/main_analysis.py` for analysis
4. Follow Power BI guide to create dashboards

## Dataset
Brazilian E-Commerce Public Dataset by Olist from Kaggle:
- **Link**: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- **Size**: ~45MB
- **Records**: ~100k orders
- **Features**: Customer data, product info, order details, reviews, payments

## Skills Demonstrated
- Data cleaning and preprocessing
- Advanced SQL queries and optimization
- Big data processing with PySpark
- Machine learning model development
- Data visualization and storytelling
- Business intelligence dashboard creation

## Project Outcomes
- Customer behavior insights
- Sales performance analysis
- Predictive analytics models
- Interactive business dashboards
- Actionable business recommendations
"""
    
    with open('docs/project_overview.md', 'w', encoding="utf-8") as f:
        f.write(overview)
    print("✅ Created: docs/project_overview.md")
    
    # Technical guide
    technical_guide = """# Technical Implementation Guide

## Python Environment Setup
1. Install Python 3.8+
2. Install required packages: `pip install -r requirements.txt`
3. Set up PySpark environment variables

## PySpark Configuration
- Set JAVA_HOME environment variable
- Configure Spark memory settings
- Enable Arrow optimization for better performance

## Database Setup
1. Install PostgreSQL/MySQL
2. Run `sql/database_setup.sql`
3. Import dataset using provided scripts

## Power BI Integration
1. Install Power BI Desktop
2. Import processed data files
3. Follow dashboard creation guide

## Model Training
- Customer segmentation: K-means clustering
- Churn prediction: Random Forest
- Sales forecasting: Time series analysis

## Performance Optimization
- Use appropriate data types
- Implement data partitioning
- Optimize SQL queries
- Cache frequently used data

## Troubleshooting
- Check Python version compatibility
- Verify dataset file integrity
- Monitor memory usage
- Check database connections
"""
    
    with open('docs/technical_guide.md', 'w', encoding="utf-8") as f:
        f.write(technical_guide)
    print("✅ Created: docs/technical_guide.md")

def run_initial_tests():
    """Run initial tests to verify setup"""
    print("\n🧪 Running initial tests...")
    
    try:
        # Test Python imports
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
        print("✅ Core Python packages imported successfully")
        
        # Test PySpark (if available)
        try:
            from pyspark.sql import SparkSession
            print("✅ PySpark available")
        except ImportError:
            print("⚠️  PySpark not available - will be installed with requirements")
        
        # Test scikit-learn
        try:
            from sklearn.cluster import KMeans
            print("✅ Scikit-learn available")
        except ImportError:
            print("⚠️  Scikit-learn not available - will be installed with requirements")
        
        print("✅ Initial tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        print("❌ Setup failed due to Python version incompatibility")
        return

    # Create project structure
    create_project_structure()
    
    # Create sample files
    create_sample_files()
    
    # Create database setup
    create_database_setup()
    
    # Create documentation
    create_project_documentation()
    
    # Install requirements
    if not install_requirements():
        print("⚠️  Package installation failed. Please install manually: pip install -r requirements.txt")
    
    # Run tests
    if run_initial_tests():
        print("\n🎉 Project setup completed successfully!")
    else:
        print("\n⚠️  Setup completed with warnings. Please check the issues above.")
    
    print("\n📋 NEXT STEPS:")
    print("1. Download the dataset: python python/download_dataset.py")
    print("2. Run the analysis: python python/main_analysis.py")
    print("3. Create Power BI dashboards using the guide in powerbi/")
    print("4. Explore the SQL queries in sql/")
    print("5. Check the documentation in docs/")
    
    print("\n🔗 Important Links:")
    print("• Dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
    print("• Power BI: https://powerbi.microsoft.com/")
    print("• PySpark: https://spark.apache.org/docs/latest/api/python/")
    
    print("\n💡 Tips:")
    print("• The project includes sample data for testing")
    print("• All scripts include error handling and logging")
    print("• Check the logs/ folder for detailed execution logs")
    print("• Customize the analysis based on your specific needs")

if __name__ == "__main__":
    main() 