#!/usr/bin/env python3
"""
Business Analytics & Machine Learning Project
Interactive Analysis Script (Can be converted to Jupyter notebook)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("✅ Libraries imported successfully!")

def load_data():
    """Load and prepare the datasets"""
    try:
        # Load main datasets
        orders_df = pd.read_csv('data/olist_orders_dataset.csv')
        customers_df = pd.read_csv('data/olist_customers_dataset.csv')
        products_df = pd.read_csv('data/olist_products_dataset.csv')
        order_items_df = pd.read_csv('data/olist_order_items_dataset.csv')
        payments_df = pd.read_csv('data/olist_order_payments_dataset.csv')
        reviews_df = pd.read_csv('data/olist_order_reviews_dataset.csv')
        
        print("✅ All datasets loaded successfully!")
        print(f"📊 Orders: {orders_df.shape}")
        print(f"👥 Customers: {customers_df.shape}")
        print(f"📦 Products: {products_df.shape}")
        
        return orders_df, customers_df, products_df, order_items_df, payments_df, reviews_df
        
    except FileNotFoundError:
        print("❌ Dataset files not found. Please download the dataset from Kaggle first.")
        print("🔗 Link: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
        return None, None, None, None, None, None

def preprocess_data(orders_df, customers_df, products_df, order_items_df, payments_df, reviews_df):
    """Clean and preprocess the data"""
    print("🔄 Starting data preprocessing...")
    
    if 'order_purchase_date' not in orders_df.columns and 'order_purchase_timestamp' in orders_df.columns:
        orders_df['order_purchase_date'] = pd.to_datetime(orders_df['order_purchase_timestamp']).dt.date
    # Convert date columns
    orders_df['order_purchase_date'] = pd.to_datetime(orders_df['order_purchase_date'])
    orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])
    
    # Merge datasets for analysis
    main_df = orders_df.merge(customers_df, on='customer_id', how='left')
    main_df = main_df.merge(order_items_df, on='order_id', how='left')
    main_df = main_df.merge(products_df, on='product_id', how='left')
    main_df = main_df.merge(payments_df, on='order_id', how='left')
    main_df = main_df.merge(reviews_df, on='order_id', how='left')
    
    # Handle missing values
    main_df['review_score'] = main_df['review_score'].fillna(main_df['review_score'].median())
    main_df['product_category_name'] = main_df['product_category_name'].fillna('Unknown')
    
    print(f"✅ Data preprocessing completed! Merged dataset shape: {main_df.shape}")
    return main_df

def customer_analysis(main_df):
    """Perform customer analysis and segmentation"""
    print("🔄 Performing customer analysis...")
    
    # Calculate customer metrics
    customer_metrics = main_df.groupby('customer_id').agg({
        'order_id': 'count',
        'payment_value': ['sum', 'mean'],
        'order_purchase_date': ['min', 'max'],
        'review_score': ['count', 'mean']
    }).round(2)
    
    # Flatten column names
    customer_metrics.columns = ['total_orders', 'total_spent', 'avg_order_value', 
                               'first_order_date', 'last_order_date', 'total_reviews', 'avg_review_score']
    
    # Calculate customer lifespan
    customer_metrics['customer_lifespan_days'] = (
        customer_metrics['last_order_date'] - customer_metrics['first_order_date']
    ).dt.days
    
    # Customer segmentation using K-means
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    
    features = ['total_orders', 'total_spent', 'avg_order_value', 'total_reviews', 'avg_review_score']
    X = customer_metrics[features].fillna(0)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    customer_metrics['cluster'] = kmeans.fit_predict(X_scaled)
    
    print("✅ Customer analysis completed!")
    return customer_metrics, kmeans, scaler

def sales_analysis(main_df):
    """Perform sales analysis and forecasting"""
    print("🔄 Performing sales analysis...")
    
    # Daily sales analysis
    daily_sales = main_df.groupby('order_purchase_date')['payment_value'].sum().reset_index()
    daily_sales.columns = ['date', 'revenue']
    daily_sales = daily_sales.sort_values('date')
    
    # Monthly aggregation
    monthly_sales = daily_sales.set_index('date').resample('M').sum().reset_index()
    monthly_sales['month'] = monthly_sales['date'].dt.strftime('%Y-%m')
    
    print(f"✅ Sales analysis completed!")
    print(f"Total revenue: R$ {daily_sales['revenue'].sum():,.2f}")
    print(f"Average daily revenue: R$ {daily_sales['revenue'].mean():,.2f}")
    
    return daily_sales, monthly_sales

def product_analysis(main_df):
    """Analyze product performance"""
    print("🔄 Performing product analysis...")
    
    # Product category analysis
    product_performance = main_df.groupby('product_category_name').agg({
        'order_id': 'count',
        'payment_value': ['sum', 'mean'],
        'review_score': 'mean',
        'customer_id': 'nunique'
    }).round(2)
    
    product_performance.columns = ['total_orders', 'total_revenue', 'avg_price', 'avg_rating', 'unique_customers']
    product_performance = product_performance.sort_values('total_revenue', ascending=False)
    
    print("✅ Product analysis completed!")
    return product_performance

def churn_prediction(customer_metrics):
    """Build churn prediction model"""
    print("🔄 Building churn prediction model...")
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, accuracy_score
    
    # Define churn (customers who haven't ordered in last 90 days)
    cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=90)
    customer_metrics['is_churned'] = (customer_metrics['last_order_date'] < cutoff_date).astype(int)
    
    # Prepare features
    features = ['total_orders', 'total_spent', 'avg_order_value', 'total_reviews', 'avg_review_score', 'customer_lifespan_days']
    X = customer_metrics[features].fillna(0)
    y = customer_metrics['is_churned']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train Random Forest model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Churn prediction model completed! Accuracy: {accuracy:.4f}")
    return rf_model, features

def geographic_analysis(main_df):
    """Analyze geographic performance"""
    print("🔄 Performing geographic analysis...")
    
    # State-wise analysis
    state_analysis = main_df.groupby('customer_state').agg({
        'customer_id': 'nunique',
        'order_id': 'count',
        'payment_value': ['sum', 'mean'],
        'review_score': 'mean'
    }).round(2)
    
    state_analysis.columns = ['unique_customers', 'total_orders', 'total_revenue', 'avg_order_value', 'avg_satisfaction']
    state_analysis = state_analysis.sort_values('total_revenue', ascending=False)
    
    print("✅ Geographic analysis completed!")
    return state_analysis

def generate_insights(customer_metrics, main_df, product_performance, state_analysis):
    """Generate business insights and recommendations"""
    print("💡 Generating business insights...")
    
    print("\n" + "="*50)
    print("BUSINESS INSIGHTS & RECOMMENDATIONS")
    print("="*50)
    
    # Customer insights
    print("\n👥 CUSTOMER INSIGHTS:")
    print(f"• Total customers analyzed: {len(customer_metrics):,}")
    print(f"• Average customer lifetime value: R$ {customer_metrics['total_spent'].mean():,.2f}")
    print(f"• Customer churn rate: {customer_metrics['is_churned'].mean():.2%}")
    print(f"• Most valuable customer segment: Cluster {customer_metrics.groupby('cluster')['total_spent'].mean().idxmax()}")
    
    # Sales insights
    print("\n💰 SALES INSIGHTS:")
    print(f"• Total revenue: R$ {main_df['payment_value'].sum():,.2f}")
    print(f"• Average order value: R$ {main_df['payment_value'].mean():,.2f}")
    print(f"• Best performing category: {product_performance.index[0]}")
    print(f"• Top state by revenue: {state_analysis.index[0]}")
    
    # Operational insights
    print("\n⚙️ OPERATIONAL INSIGHTS:")
    print(f"• Total orders: {len(main_df):,}")
    print(f"• Average customer satisfaction: {main_df['review_score'].mean():.2f}/5.0")
    print(f"• Delivery success rate: {(main_df['order_status'] == 'delivered').mean():.2%}")
    
    print("\n🎯 STRATEGIC RECOMMENDATIONS:")
    print("1. Focus on high-value customer segments (Clusters 0 & 1)")
    print("2. Implement retention strategies for customers at risk of churn")
    print("3. Expand product offerings in top-performing categories")
    print("4. Optimize operations in high-revenue states")
    print("5. Improve customer satisfaction to reduce churn rate")

def save_results(customer_metrics, product_performance, state_analysis, rf_model, kmeans, scaler):
    """Save models and results"""
    print("🔄 Saving results and models...")
    
    import joblib
    import os
    
    # Create output directory
    os.makedirs('../ml_models', exist_ok=True)
    
    # Save models
    joblib.dump(rf_model, '../ml_models/churn_prediction_model.pkl')
    joblib.dump(scaler, '../ml_models/feature_scaler.pkl')
    joblib.dump(kmeans, '../ml_models/customer_segmentation_model.pkl')
    
    # Save processed data
    customer_metrics.to_csv('../data/processed_customer_metrics.csv')
    product_performance.to_csv('../data/processed_product_performance.csv')
    state_analysis.to_csv('../data/processed_state_analysis.csv')
    
    print("✅ Models and data saved successfully!")
    print("📁 Files saved to:")
    print("   • ../ml_models/")
    print("   • ../data/")

def main():
    """Main execution function"""
    print("🚀 Starting Business Analytics & ML Project...")
    
    # Load data
    orders_df, customers_df, products_df, order_items_df, payments_df, reviews_df = load_data()
    if orders_df is None:
        return
    
    # Preprocess data
    main_df = preprocess_data(orders_df, customers_df, products_df, order_items_df, payments_df, reviews_df)
    
    # Perform analysis
    customer_metrics, kmeans, scaler = customer_analysis(main_df)
    daily_sales, monthly_sales = sales_analysis(main_df)
    product_performance = product_analysis(main_df)
    rf_model, features = churn_prediction(customer_metrics)
    state_analysis = geographic_analysis(main_df)
    
    # Generate insights
    generate_insights(customer_metrics, main_df, product_performance, state_analysis)
    
    # Save results
    save_results(customer_metrics, product_performance, state_analysis, rf_model, kmeans, scaler)
    
    print("\n🎉 Analysis completed! The project is ready for Power BI integration.")

if __name__ == "__main__":
    main() 