-- Business Analytics & Machine Learning Project
-- Advanced SQL Analysis Queries
-- Dataset: Brazilian E-Commerce Public Dataset by Olist

-- =====================================================
-- 1. CUSTOMER ANALYSIS & SEGMENTATION
-- =====================================================

-- Customer Lifetime Value Analysis
WITH customer_metrics AS (
    SELECT 
        c.customer_id,
        c.customer_city,
        c.customer_state,
        COUNT(DISTINCT o.order_id) as total_orders,
        SUM(oi.price + oi.freight_value) as total_spent,
        AVG(oi.price + oi.freight_value) as avg_order_value,
        MAX(o.order_purchase_date) as last_order_date,
        MIN(o.order_purchase_date) as first_order_date,
        DATEDIFF(MAX(o.order_purchase_date), MIN(o.order_purchase_date)) as customer_lifespan_days,
        COUNT(r.review_score) as total_reviews,
        AVG(r.review_score) as avg_review_score
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN order_reviews r ON o.order_id = r.order_id
    GROUP BY c.customer_id, c.customer_city, c.customer_state
    HAVING total_orders > 0
),
customer_segments AS (
    SELECT 
        *,
        CASE 
            WHEN total_spent >= 1000 AND total_orders >= 5 THEN 'High-Value Loyal'
            WHEN total_spent >= 500 AND total_orders >= 3 THEN 'Medium-Value Active'
            WHEN total_spent >= 200 AND total_orders >= 2 THEN 'Low-Value Regular'
            ELSE 'Occasional Buyer'
        END as customer_segment,
        CASE 
            WHEN avg_review_score >= 4.5 THEN 'Very Satisfied'
            WHEN avg_review_score >= 4.0 THEN 'Satisfied'
            WHEN avg_review_score >= 3.0 THEN 'Neutral'
            ELSE 'Dissatisfied'
        END as satisfaction_level
    FROM customer_metrics
)
SELECT 
    customer_segment,
    satisfaction_level,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_lifetime_value,
    AVG(total_orders) as avg_orders,
    AVG(avg_review_score) as avg_satisfaction
FROM customer_segments
GROUP BY customer_segment, satisfaction_level
ORDER BY avg_lifetime_value DESC;

-- =====================================================
-- 2. SALES PERFORMANCE ANALYSIS
-- =====================================================

-- Monthly Sales Trend Analysis
SELECT 
    DATE_FORMAT(o.order_purchase_date, '%Y-%m') as month,
    COUNT(DISTINCT o.order_id) as total_orders,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    SUM(oi.price + oi.freight_value) as total_revenue,
    AVG(oi.price + oi.freight_value) as avg_order_value,
    SUM(oi.freight_value) as total_freight_revenue,
    (SUM(oi.price + oi.freight_value) - SUM(oi.freight_value)) as net_product_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY DATE_FORMAT(o.order_purchase_date, '%Y-%m')
ORDER BY month;

-- Product Category Performance
SELECT 
    p.product_category_name,
    COUNT(DISTINCT o.order_id) as total_orders,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    SUM(oi.price) as total_revenue,
    AVG(oi.price) as avg_product_price,
    AVG(r.review_score) as avg_rating,
    COUNT(r.review_score) as review_count
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
HAVING total_orders >= 10
ORDER BY total_revenue DESC
LIMIT 20;

-- =====================================================
-- 3. GEOGRAPHICAL ANALYSIS
-- =====================================================

-- State-wise Performance Analysis
SELECT 
    c.customer_state,
    COUNT(DISTINCT c.customer_id) as total_customers,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(oi.price + oi.freight_value) as total_revenue,
    AVG(oi.price + oi.freight_value) as avg_order_value,
    AVG(r.review_score) as avg_satisfaction
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;

-- City Performance Analysis (Top 20)
SELECT 
    c.customer_city,
    c.customer_state,
    COUNT(DISTINCT c.customer_id) as total_customers,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(oi.price + oi.freight_value) as total_revenue,
    AVG(oi.price + oi.freight_value) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_city, c.customer_state
HAVING total_orders >= 50
ORDER BY total_revenue DESC
LIMIT 20;

-- =====================================================
-- 4. PAYMENT & FINANCIAL ANALYSIS
-- =====================================================

-- Payment Method Analysis
SELECT 
    op.payment_type,
    COUNT(*) as payment_count,
    SUM(op.payment_value) as total_payment_value,
    AVG(op.payment_value) as avg_payment_value,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    AVG(r.review_score) as avg_satisfaction
FROM order_payments op
JOIN orders o ON op.order_id = o.order_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY op.payment_type
ORDER BY total_payment_value DESC;

-- Payment Installment Analysis
SELECT 
    op.payment_installments,
    COUNT(*) as order_count,
    SUM(op.payment_value) as total_revenue,
    AVG(op.payment_value) as avg_order_value,
    AVG(r.review_score) as avg_satisfaction
FROM order_payments op
JOIN orders o ON op.order_id = o.order_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
    AND op.payment_installments > 1
GROUP BY op.payment_installments
ORDER BY op.payment_installments;

-- =====================================================
-- 5. OPERATIONAL METRICS
-- =====================================================

-- Order Status Distribution
SELECT 
    order_status,
    COUNT(*) as order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as percentage
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;

-- Delivery Performance Analysis
SELECT 
    DATE_FORMAT(o.order_purchase_date, '%Y-%m') as month,
    COUNT(*) as total_orders,
    AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_date)) as avg_delivery_days,
    COUNT(CASE WHEN o.order_status = 'delivered' THEN 1 END) as delivered_orders,
    COUNT(CASE WHEN o.order_status = 'shipped' THEN 1 END) as shipped_orders,
    COUNT(CASE WHEN o.order_status = 'processing' THEN 1 END) as processing_orders
FROM orders o
WHERE o.order_purchase_date IS NOT NULL
GROUP BY DATE_FORMAT(o.order_purchase_date, '%Y-%m')
ORDER BY month;

-- =====================================================
-- 6. ADVANCED ANALYTICS QUERIES
-- =====================================================

-- Customer Cohort Analysis (Monthly Retention)
WITH cohort_data AS (
    SELECT 
        customer_id,
        DATE_FORMAT(MIN(order_purchase_date), '%Y-%m') as cohort_month,
        DATE_FORMAT(order_purchase_date, '%Y-%m') as order_month,
        COUNT(DISTINCT order_id) as orders_in_month
    FROM orders
    WHERE order_status = 'delivered'
    GROUP BY customer_id, DATE_FORMAT(order_purchase_date, '%Y-%m')
),
cohort_retention AS (
    SELECT 
        cohort_month,
        order_month,
        COUNT(DISTINCT customer_id) as customers,
        ROUND(COUNT(DISTINCT customer_id) * 100.0 / 
              FIRST_VALUE(COUNT(DISTINCT customer_id)) OVER (PARTITION BY cohort_month ORDER BY order_month), 2) as retention_rate
    FROM cohort_data
    GROUP BY cohort_month, order_month
)
SELECT * FROM cohort_retention
ORDER BY cohort_month, order_month;

-- Product Recommendation Query (Based on Purchase Patterns)
WITH customer_product_pairs AS (
    SELECT DISTINCT
        o1.customer_id,
        oi1.product_id,
        p1.product_category_name
    FROM orders o1
    JOIN order_items oi1 ON o1.order_id = oi1.order_id
    JOIN products p1 ON oi1.product_id = p1.product_id
    WHERE o1.order_status = 'delivered'
),
similar_customers AS (
    SELECT 
        cp1.customer_id as customer1,
        cp2.customer_id as customer2,
        COUNT(DISTINCT cp1.product_category_name) as common_categories
    FROM customer_product_pairs cp1
    JOIN customer_product_pairs cp2 ON cp1.product_category_name = cp2.product_category_name
    WHERE cp1.customer_id != cp2.customer_id
    GROUP BY cp1.customer_id, cp2.customer_id
    HAVING common_categories >= 2
)
SELECT 
    sc.customer1,
    sc.customer2,
    sc.common_categories,
    COUNT(DISTINCT cp.product_category_name) as total_categories_customer1
FROM similar_customers sc
JOIN customer_product_pairs cp ON sc.customer1 = cp.customer_id
GROUP BY sc.customer1, sc.customer2, sc.common_categories
HAVING common_categories >= 3
ORDER BY common_categories DESC, total_categories_customer1 DESC
LIMIT 50;

-- =====================================================
-- 7. PERFORMANCE OPTIMIZATION QUERIES
-- =====================================================

-- Create indexes for better performance (run these separately)
-- CREATE INDEX idx_orders_customer_id ON orders(customer_id);
-- CREATE INDEX idx_orders_purchase_date ON orders(order_purchase_date);
-- CREATE INDEX idx_order_items_order_id ON order_items(order_id);
-- CREATE INDEX idx_products_category ON products(product_category_name);
-- CREATE INDEX idx_payments_order_id ON order_payments(order_id);
-- CREATE INDEX idx_reviews_order_id ON order_reviews(order_id);

-- =====================================================
-- 8. SUMMARY METRICS FOR DASHBOARD
-- =====================================================

-- Key Performance Indicators (KPIs)
SELECT 
    'Total Customers' as metric,
    COUNT(DISTINCT c.customer_id) as value
FROM customers c
UNION ALL
SELECT 
    'Total Orders' as metric,
    COUNT(DISTINCT o.order_id) as value
FROM orders o
UNION ALL
SELECT 
    'Total Revenue' as metric,
    ROUND(SUM(oi.price + oi.freight_value), 2) as value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
UNION ALL
SELECT 
    'Average Order Value' as metric,
    ROUND(AVG(oi.price + oi.freight_value), 2) as value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
UNION ALL
SELECT 
    'Customer Satisfaction' as metric,
    ROUND(AVG(r.review_score), 2) as value
FROM order_reviews r
UNION ALL
SELECT 
    'Delivery Success Rate' as metric,
    ROUND(COUNT(CASE WHEN o.order_status = 'delivered' THEN 1 END) * 100.0 / COUNT(*), 2) as value
FROM orders o; 