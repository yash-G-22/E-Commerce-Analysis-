#!/usr/bin/env python3
"""
Business Analytics & Machine Learning Project
Main Analysis Script using PySpark and ML techniques
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# PySpark imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
from pyspark.ml.clustering import KMeans
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import ClusteringEvaluator, RegressionEvaluator, MulticlassClassificationEvaluator

# ML imports
from sklearn.cluster import KMeans as SklearnKMeans
from sklearn.ensemble import RandomForestClassifier as SklearnRF
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler as SklearnScaler
import joblib

class BusinessAnalytics:
    def __init__(self):
        """Initialize Spark session and load data"""
        self.spark = SparkSession.builder \
            .appName("BusinessAnalytics") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .getOrCreate()
        
        self.spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
        print("✅ Spark session initialized successfully!")
        
    def load_data(self, data_path="data/"):
        """Load and prepare the dataset"""
        try:
            # Load main datasets
            self.orders_df = self.spark.read.csv(f"{data_path}olist_orders_dataset.csv", header=True, inferSchema=True)
            self.customers_df = self.spark.read.csv(f"{data_path}olist_customers_dataset.csv", header=True, inferSchema=True)
            self.products_df = self.spark.read.csv(f"{data_path}olist_products_dataset.csv", header=True, inferSchema=True)
            self.order_items_df = self.spark.read.csv(f"{data_path}olist_order_items_dataset.csv", header=True, inferSchema=True)
            self.payments_df = self.spark.read.csv(f"{data_path}olist_order_payments_dataset.csv", header=True, inferSchema=True)
            self.reviews_df = self.spark.read.csv(f"{data_path}olist_order_reviews_dataset.csv", header=True, inferSchema=True)
            
            print("✅ All datasets loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def data_preprocessing(self):
        """Clean and preprocess the data"""
        print("🔄 Starting data preprocessing...")
        
        # Convert date columns
        self.orders_df = self.orders_df.withColumn("order_purchase_date", 
            to_date(col("order_purchase_timestamp")))
        
        # Join datasets for analysis
        self.main_df = self.orders_df \
            .join(self.customers_df, "customer_id", "left") \
            .join(self.order_items_df, "order_id", "left") \
            .join(self.products_df, "product_id", "left") \
            .join(self.payments_df, "order_id", "left") \
            .join(self.reviews_df, "order_id", "left")
        
        # Calculate customer metrics
        self.customer_metrics = self.main_df.groupBy("customer_id") \
            .agg(
                count("order_id").alias("total_orders"),
                sum("payment_value").alias("total_spent"),
                avg("payment_value").alias("avg_order_value"),
                max("order_purchase_date").alias("last_order_date"),
                count("review_score").alias("total_reviews"),
                avg("review_score").alias("avg_review_score")
            )
        
        print("✅ Data preprocessing completed!")
        return self.customer_metrics
    
    def customer_segmentation(self, n_clusters=4):
        """Perform customer segmentation using K-means clustering"""
        print(f"🔄 Performing customer segmentation with {n_clusters} clusters...")
        
        # Prepare features for clustering
        features_col = "features"
        assembler = VectorAssembler(
            inputCols=["total_orders", "total_spent", "avg_order_value", "total_reviews", "avg_review_score"],
            outputCol=features_col, handleInvalid="skip"
        )
        
        # Scale features
        scaler = StandardScaler(inputCol=features_col, outputCol="scaled_features")
        
        # K-means clustering
        kmeans = KMeans(k=n_clusters, seed=42, featuresCol="scaled_features")
        
        # Pipeline
        from pyspark.ml import Pipeline
        pipeline = Pipeline(stages=[assembler, scaler, kmeans])
        
        # Fit model
        model = pipeline.fit(self.customer_metrics)
        self.segmentation_model = model
        
        # Predict clusters
        self.customer_segments = model.transform(self.customer_metrics)
        
        # Evaluate clustering
        evaluator = ClusteringEvaluator()
        silhouette = evaluator.evaluate(self.customer_segments)
        
        print(f"✅ Customer segmentation completed! Silhouette score: {silhouette:.4f}")
        return self.customer_segments
    
    def sales_forecasting(self):
        """Perform sales forecasting using time series analysis"""
        print("🔄 Performing sales forecasting...")
        
        # Aggregate daily sales
        daily_sales = self.main_df.groupBy("order_purchase_date") \
            .agg(sum("payment_value").alias("daily_revenue")) \
            .orderBy("order_purchase_date")
        
        # Convert to pandas for Prophet
        daily_sales_pd = daily_sales.toPandas()
        daily_sales_pd.columns = ['ds', 'y']
        
        # Simple moving average forecast (since Prophet requires additional setup)
        daily_sales_pd['forecast_7d'] = daily_sales_pd['y'].rolling(window=7).mean()
        daily_sales_pd['forecast_30d'] = daily_sales_pd['y'].rolling(window=30).mean()
        
        self.sales_forecast = daily_sales_pd
        print("✅ Sales forecasting completed!")
        return self.sales_forecast
    
    def churn_prediction(self):
        """Predict customer churn using Random Forest"""
        print("🔄 Building churn prediction model...")
        
        # Define churn (customers who haven't ordered in last 90 days)
        cutoff_date = datetime.now() - timedelta(days=90)
        
        churn_data = self.customer_metrics.withColumn("is_churned",
            when(col("last_order_date") < cutoff_date, 1).otherwise(0))
        
        # Prepare features
        feature_cols = ["total_orders", "total_spent", "avg_order_value", "total_reviews", "avg_review_score"]
        assembler = VectorAssembler(inputCols=feature_cols, outputCol="features", handleInvalid="skip")
        
        # Random Forest for classification
        rf = RandomForestClassifier(labelCol="is_churned", featuresCol="features", numTrees=100, seed=42)
        
        # Pipeline
        from pyspark.ml import Pipeline
        pipeline = Pipeline(stages=[assembler, rf])
        
        # Split data
        train_data, test_data = churn_data.randomSplit([0.8, 0.2], seed=42)
        
        # Train model
        self.churn_model = pipeline.fit(train_data)
        
        # Predictions
        predictions = self.churn_model.transform(test_data)
        
        # Evaluate model
        evaluator = MulticlassClassificationEvaluator(labelCol="is_churned", predictionCol="prediction", metricName="accuracy")
        accuracy = evaluator.evaluate(predictions)
        
        print(f"✅ Churn prediction model completed! Accuracy: {accuracy:.4f}")
        return predictions
    
    def product_recommendation(self):
        """Simple product recommendation system"""
        print("🔄 Building product recommendation system...")
        
        # Calculate product popularity
        product_popularity = self.main_df.groupBy("product_id", "product_category_name") \
            .agg(
                count("order_id").alias("order_count"),
                avg("payment_value").alias("avg_price"),
                avg("review_score").alias("avg_rating")
            )
        
        # Calculate product similarity (simple approach)
        self.product_recommendations = product_popularity.orderBy(desc("order_count"))
        
        print("✅ Product recommendation system completed!")
        return self.product_recommendations
    
    def generate_insights(self):
        """Generate business insights and recommendations"""
        print("🔄 Generating business insights...")
        
        insights = {
            "total_customers": self.customer_metrics.count(),
            "total_revenue": self.customer_metrics.agg(sum("total_spent")).collect()[0][0],
            "avg_customer_lifetime_value": self.customer_metrics.agg(avg("total_spent")).collect()[0][0],
            "top_performing_products": self.product_recommendations.limit(10).toPandas().to_dict('records'),
            "customer_segments": self.customer_segments.groupBy("prediction").count().toPandas().to_dict('records')
        }
        
        print("✅ Business insights generated!")
        return insights
    
    def save_models(self, output_path="ml_models/"):
        """Save trained models for later use"""
        os.makedirs(output_path, exist_ok=True)
        
        # Save PySpark models
        self.segmentation_model.write().overwrite().save(f"{output_path}customer_segmentation_model")
        self.churn_model.write().overwrite().save(f"{output_path}churn_prediction_model")
        
        print(f"✅ Models saved to {output_path}")
    
    def cleanup(self):
        """Clean up Spark session"""
        if self.spark:
            self.spark.stop()
            print("✅ Spark session stopped")

def main():
    """Main execution function"""
    print("🚀 Starting Business Analytics & ML Project...")
    
    # Initialize analytics
    analytics = BusinessAnalytics()
    
    try:
        # Load data
        if not analytics.load_data():
            print("❌ Failed to load data. Please check data path.")
            return
        
        # Perform analysis
        analytics.data_preprocessing()
        analytics.customer_segmentation()
        analytics.sales_forecasting()
        analytics.churn_prediction()
        analytics.product_recommendation()
        
        # Generate insights
        insights = analytics.generate_insights()
        
        # Save models
        analytics.save_models()
        
        print("\n🎉 Analysis completed successfully!")
        print(f"📊 Total customers analyzed: {insights['total_customers']}")
        print(f"💰 Total revenue: R$ {insights['total_revenue']:,.2f}")
        print(f"📈 Average customer lifetime value: R$ {insights['avg_customer_lifetime_value']:,.2f}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
    finally:
        analytics.cleanup()

if __name__ == "__main__":
    main() 