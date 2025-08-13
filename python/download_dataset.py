#!/usr/bin/env python3
"""
Dataset Download Script for Business Analytics Project
Downloads and prepares the Brazilian E-Commerce Public Dataset by Olist
"""

import os
import requests
import zipfile
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def create_directories():
    """Create necessary project directories"""
    directories = [
        'data',
        'ml_models',
        'outputs',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def download_dataset():
    """
    Download the Brazilian E-Commerce dataset from Kaggle
    Note: This requires Kaggle API credentials
    """
    print("🔗 Attempting to download dataset from Kaggle...")
    
    try:
        # Try using Kaggle API
        import kaggle
        
        # Download the dataset
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            'olistbr/brazilian-ecommerce',
            path='data',
            unzip=True
        )
        print("✅ Dataset downloaded successfully using Kaggle API!")
        return True
        
    except ImportError:
        print("⚠️  Kaggle package not installed. Installing...")
        os.system("pip install kaggle")
        
        try:
            import kaggle
            kaggle.api.authenticate()
            kaggle.api.dataset_download_files(
                'olistbr/brazilian-ecommerce',
                path='data',
                unzip=True
            )
            print("✅ Dataset downloaded successfully using Kaggle API!")
            return True
        except Exception as e:
            print(f"❌ Kaggle API error: {e}")
            return False
    
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return False

def download_manual_links():
    """
    Provide manual download links if automatic download fails
    """
    print("\n📥 MANUAL DOWNLOAD INSTRUCTIONS:")
    print("=" * 50)
    print("If automatic download fails, please follow these steps:")
    print("\n1. Visit: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
    print("2. Click 'Download' button")
    print("3. Extract the ZIP file to the 'data/' folder")
    print("4. Ensure the following files are present:")
    
    required_files = [
        'olist_orders_dataset.csv',
        'olist_customers_dataset.csv',
        'olist_products_dataset.csv',
        'olist_order_items_dataset.csv',
        'olist_order_payments_dataset.csv',
        'olist_order_reviews_dataset.csv',
        'olist_sellers_dataset.csv',
        'olist_geolocation_dataset.csv'
    ]
    
    for file in required_files:
        print(f"   • {file}")
    
    print("\n5. Run this script again to verify the files")
    print("\nNote: You may need to create a Kaggle account and accept the dataset terms")

def verify_dataset():
    """Verify that all required dataset files are present"""
    print("\n🔍 Verifying dataset files...")
    
    required_files = [
        'olist_orders_dataset.csv',
        'olist_customers_dataset.csv',
        'olist_products_dataset.csv',
        'olist_order_items_dataset.csv',
        'olist_order_payments_dataset.csv',
        'olist_order_reviews_dataset.csv',
        'olist_sellers_dataset.csv',
        'olist_geolocation_dataset.csv'
    ]
    
    missing_files = []
    present_files = []
    
    for file in required_files:
        file_path = Path('data') / file
        if file_path.exists():
            present_files.append(file)
            # Get file size
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"✅ {file} ({size_mb:.1f} MB)")
        else:
            missing_files.append(file)
            print(f"❌ {file} - MISSING")
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} files:")
        for file in missing_files:
            print(f"   • {file}")
        return False
    else:
        print(f"\n🎉 All {len(present_files)} dataset files are present!")
        return True

def create_sample_data():
    """Create sample data files for testing if dataset is not available"""
    print("\n🔄 Creating sample data files for testing...")
    
    # Sample orders data
    sample_orders = pd.DataFrame({
        'order_id': [f'order_{i:03d}' for i in range(1, 101)],
        'customer_id': [f'customer_{i:03d}' for i in range(1, 101)],
        'order_status': ['delivered'] * 80 + ['shipped'] * 15 + ['processing'] * 5,
        'order_purchase_date': pd.date_range('2023-01-01', periods=100, freq='D'),
        'order_delivered_customer_date': pd.date_range('2023-01-03', periods=100, freq='D'),
        'order_estimated_delivery_date': pd.date_range('2023-01-05', periods=100, freq='D')
    })
    
    # Sample customers data
    sample_customers = pd.DataFrame({
        'customer_id': [f'customer_{i:03d}' for i in range(1, 101)],
        'customer_unique_id': [f'unique_{i:03d}' for i in range(1, 101)],
        'customer_zip_code_prefix': [f'{i:05d}' for i in range(10000, 10100)],
        'customer_city': ['São Paulo'] * 30 + ['Rio de Janeiro'] * 25 + ['Belo Horizonte'] * 20 + ['Salvador'] * 15 + ['Brasília'] * 10,
        'customer_state': ['SP'] * 30 + ['RJ'] * 25 + ['MG'] * 20 + ['BA'] * 15 + ['DF'] * 10
    })
    
    # Sample products data
    sample_products = pd.DataFrame({
        'product_id': [f'product_{i:03d}' for i in range(1, 101)],
        'product_category_name': ['electronics'] * 20 + ['clothing'] * 25 + ['home'] * 20 + ['sports'] * 15 + ['books'] * 20,
        'product_name_lenght': np.random.randint(10, 50, 100),
        'product_description_lenght': np.random.randint(50, 200, 100),
        'product_photos_qty': np.random.randint(1, 5, 100),
        'product_weight_g': np.random.randint(100, 2000, 100),
        'product_length_cm': np.random.randint(10, 100, 100),
        'product_height_cm': np.random.randint(5, 50, 100),
        'product_width_cm': np.random.randint(10, 100, 100)
    })
    
    # Sample order items data
    sample_order_items = pd.DataFrame({
        'order_id': [f'order_{i:03d}' for i in range(1, 101)],
        'order_item_id': [1] * 100,
        'product_id': [f'product_{i:03d}' for i in range(1, 101)],
        'seller_id': [f'seller_{i:03d}' for i in range(1, 101)],
        'shipping_limit_date': pd.date_range('2023-01-05', periods=100, freq='D'),
        'price': np.random.uniform(10, 500, 100).round(2),
        'freight_value': np.random.uniform(5, 50, 100).round(2)
    })
    
    # Sample payments data
    sample_payments = pd.DataFrame({
        'order_id': [f'order_{i:03d}' for i in range(1, 101)],
        'payment_sequential': [1] * 100,
        'payment_type': ['credit_card'] * 60 + ['boleto'] * 25 + ['voucher'] * 10 + ['debit_card'] * 5,
        'payment_installments': np.random.randint(1, 12, 100),
        'payment_value': np.random.uniform(15, 550, 100).round(2)
    })
    
    # Sample reviews data
    sample_reviews = pd.DataFrame({
        'review_id': [f'review_{i:03d}' for i in range(1, 101)],
        'order_id': [f'order_{i:03d}' for i in range(1, 101)],
        'review_score': np.random.choice([1, 2, 3, 4, 5], 100, p=[0.05, 0.1, 0.15, 0.3, 0.4]),
        'review_comment_title': ['Great product!'] * 40 + ['Good quality'] * 30 + ['Average'] * 20 + ['Could be better'] * 10,
        'review_comment_message': ['Excellent service and product quality'] * 100,
        'review_creation_date': pd.date_range('2023-01-01', periods=100, freq='D'),
        'review_answer_timestamp': pd.date_range('2023-01-02', periods=100, freq='D')
    })
    
    # Save sample data
    sample_orders.to_csv('data/olist_orders_dataset.csv', index=False)
    sample_customers.to_csv('data/olist_customers_dataset.csv', index=False)
    sample_products.to_csv('data/olist_products_dataset.csv', index=False)
    sample_order_items.to_csv('data/olist_order_items_dataset.csv', index=False)
    sample_payments.to_csv('data/olist_order_payments_dataset.csv', index=False)
    sample_reviews.to_csv('data/olist_order_reviews_dataset.csv', index=False)
    
    print("✅ Sample data files created successfully!")
    print("📝 Note: These are sample files for testing. For real analysis, use the actual dataset.")

def main():
    """Main execution function"""
    print("🚀 Business Analytics Project - Dataset Setup")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Try to download dataset
    if not download_dataset():
        print("\n❌ Automatic download failed.")
        download_manual_links()
        
        # Check if files are present after manual download
        if not verify_dataset():
            print("\n🔄 Creating sample data for testing...")
            create_sample_data()
            verify_dataset()
    else:
        # Verify downloaded dataset
        verify_dataset()
    
    print("\n📋 NEXT STEPS:")
    print("1. Ensure all dataset files are in the 'data/' folder")
    print("2. Run the main analysis script: python python/main_analysis.py")
    print("3. Or run the interactive notebook: python python/business_analytics_notebook.py")
    print("4. Follow the Power BI guide to create dashboards")
    
    print("\n🔗 Dataset Information:")
    print("• Source: Brazilian E-Commerce Public Dataset by Olist")
    print("• Kaggle Link: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
    print("• Size: ~45MB")
    print("• Records: ~100k orders")
    print("• Features: Customer data, product info, order details, reviews, payments")

if __name__ == "__main__":
    main() 