# 🚀 Business Analytics & Machine Learning Project

## 📋 Project Overview

This is a comprehensive **Business Analyst Level 1** project that demonstrates advanced analytics skills using a modern tech stack. The project analyzes e-commerce data to provide actionable business insights through customer segmentation, sales forecasting, churn prediction, and interactive dashboards.

## 🛠️ Tech Stack

| Technology | Purpose | Skills Demonstrated |
|------------|---------|---------------------|
| **SQL** | Data querying, analysis, and optimization | Advanced SQL queries, performance tuning, data modeling |
| **Python (PySpark)** | Big data processing and ML | PySpark operations, distributed computing, ML pipelines |
| **Power BI** | Data visualization and dashboards | Dashboard creation, DAX measures, interactive reports |
| **Machine Learning** | Predictive analytics | K-means clustering, Random Forest, time series analysis |

## 📊 Dataset

**Brazilian E-Commerce Public Dataset by Olist**
- **Source**: [Kaggle Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Size**: ~45MB
- **Records**: ~100k orders
- **Features**: Customer data, product info, order details, reviews, payments
- **Geography**: Brazilian market data
- **Industry**: E-commerce/Retail

## 🎯 Key Features

### 1. Customer Segmentation
- **K-means clustering** for customer behavior analysis
- **4 customer segments** based on spending patterns and engagement
- **Customer lifetime value** calculation and analysis

### 2. Sales Forecasting
- **Time series analysis** for revenue prediction
- **Trend identification** and seasonal patterns
- **Moving average forecasting** for short-term predictions

### 3. Churn Prediction
- **Random Forest classifier** for customer retention
- **Feature importance analysis** for churn factors
- **Predictive modeling** with 80%+ accuracy

### 4. Product Recommendation
- **Collaborative filtering** system
- **Product performance analysis** by category
- **Customer preference mapping**

### 5. Interactive Dashboards
- **Power BI visualizations** for business stakeholders
- **Real-time KPI monitoring**
- **Drill-down capabilities** for detailed analysis

## 📁 Project Structure

```
Business Analyst/
├── 📊 data/                          # Dataset files
│   ├── olist_orders_dataset.csv      # Order information
│   ├── olist_customers_dataset.csv   # Customer details
│   ├── olist_products_dataset.csv    # Product catalog
│   ├── olist_order_items_dataset.csv # Order line items
│   ├── olist_order_payments_dataset.csv # Payment details
│   └── olist_order_reviews_dataset.csv  # Customer reviews
├── 🗄️ sql/                           # SQL analysis
│   ├── business_analysis.sql         # Comprehensive SQL queries
│   └── database_setup.sql            # Database schema setup
├── 🐍 python/                        # Python/PySpark scripts
│   ├── main_analysis.py              # Main analysis pipeline
│   ├── business_analytics_notebook.py # Interactive analysis
│   └── download_dataset.py           # Dataset downloader
├── 📈 powerbi/                       # Power BI resources
│   └── powerbi_instructions.md       # Dashboard creation guide
├── 🤖 ml_models/                     # Trained ML models
├── 📓 notebooks/                     # Jupyter notebooks
├── 📤 outputs/                       # Analysis outputs
├── 📝 logs/                          # Execution logs
├── 📚 docs/                          # Documentation
├── requirements.txt                  # Python dependencies
├── setup_project.py                  # Project setup script
└── README.md                         # Project overview
```

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+** installed
- **Power BI Desktop** (free version available)
- **Database system** (PostgreSQL/MySQL recommended)
- **Git** for version control

### Quick Start
1. **Clone/Download** the project
2. **Run setup**: `python setup_project.py`
3. **Download dataset**: `python python/download_dataset.py`
4. **Run analysis**: `python python/main_analysis.py`
5. **Create dashboards**: Follow Power BI guide

### Step-by-Step Setup

#### 1. Environment Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run project setup
python setup_project.py
```

#### 2. Dataset Preparation
```bash
# Download dataset (requires Kaggle account)
python python/download_dataset.py

# Or manually download from Kaggle and extract to data/ folder
```

#### 3. Run Analysis
```bash
# Main analysis pipeline
python python/main_analysis.py

# Interactive analysis
python python/business_analytics_notebook.py
```

#### 4. Database Setup
```sql
-- Run the database setup script
source sql/database_setup.sql

-- Import your data using the provided scripts
```

#### 5. Power BI Dashboards
- Open Power BI Desktop
- Import processed data files
- Follow the guide in `powerbi/powerbi_instructions.md`

## 📊 Analysis Pipeline

### Phase 1: Data Ingestion
- Load CSV datasets
- Validate data integrity
- Handle missing values
- Data type conversion

### Phase 2: Data Processing
- Merge multiple datasets
- Feature engineering
- Data cleaning and standardization
- Performance optimization

### Phase 3: Machine Learning
- Customer segmentation (K-means)
- Churn prediction (Random Forest)
- Sales forecasting (Time series)
- Model evaluation and validation

### Phase 4: Insights Generation
- Business metrics calculation
- Performance analysis
- Trend identification
- Actionable recommendations

### Phase 5: Visualization
- Power BI dashboard creation
- Interactive visualizations
- KPI monitoring
- Report generation

## 🎯 Business Insights

### Customer Analytics
- **Segmentation**: High-value, Medium-value, Low-value, Occasional buyers
- **Churn Risk**: Predictive modeling for customer retention
- **Lifetime Value**: Customer profitability analysis
- **Behavior Patterns**: Purchase frequency and preferences

### Sales Performance
- **Revenue Trends**: Monthly and daily patterns
- **Product Performance**: Category-wise analysis
- **Geographic Distribution**: State and city performance
- **Seasonal Patterns**: Peak and off-peak periods

### Operational Metrics
- **Delivery Performance**: Success rates and timelines
- **Payment Analysis**: Method preferences and installments
- **Customer Satisfaction**: Review scores and feedback
- **Inventory Insights**: Product demand patterns

## 💡 Skills Demonstrated

### Technical Skills
- **Data Engineering**: ETL pipelines, data cleaning, feature engineering
- **Big Data Processing**: PySpark operations, distributed computing
- **Machine Learning**: Supervised/unsupervised learning, model evaluation
- **Data Visualization**: Interactive dashboards, storytelling
- **Database Management**: SQL optimization, schema design

### Business Skills
- **Analytical Thinking**: Problem identification and solution design
- **Business Intelligence**: KPI development and monitoring
- **Predictive Analytics**: Forecasting and trend analysis
- **Stakeholder Communication**: Dashboard creation and reporting
- **Strategic Planning**: Data-driven decision making

## 🔧 Customization Options

### Data Sources
- Replace with your own e-commerce data
- Adapt to different industries (retail, healthcare, finance)
- Scale for larger datasets using PySpark

### Analysis Focus
- Modify customer segmentation criteria
- Adjust churn prediction thresholds
- Customize sales forecasting models
- Add industry-specific metrics

### Visualization
- Brand Power BI dashboards
- Create custom visualizations
- Add real-time data connections
- Implement automated reporting

## 📈 Performance Metrics

### Model Performance
- **Customer Segmentation**: Silhouette score optimization
- **Churn Prediction**: 80%+ accuracy with Random Forest
- **Sales Forecasting**: Trend prediction with moving averages
- **Product Recommendation**: Collaborative filtering effectiveness

### System Performance
- **Data Processing**: Optimized PySpark operations
- **Query Performance**: Indexed SQL queries
- **Memory Usage**: Efficient data handling
- **Scalability**: Distributed computing ready

## 🚨 Troubleshooting

### Common Issues
1. **PySpark Installation**: Ensure Java 8+ is installed
2. **Dataset Download**: Check Kaggle API credentials
3. **Memory Issues**: Adjust Spark memory settings
4. **Database Connection**: Verify connection strings and permissions

### Solutions
- Check the `logs/` folder for detailed error messages
- Verify Python package versions in `requirements.txt`
- Ensure dataset files are in the correct location
- Test database connectivity before running analysis

## 🔗 Resources & References

### Documentation
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Learning Resources
- [Kaggle Courses](https://www.kaggle.com/learn)
- [Power BI YouTube Channel](https://www.youtube.com/channel/UCyIq-4Qe7xRd9M2uy1G5LyQ)
- [DataCamp PySpark Course](https://www.datacamp.com/courses/introduction-to-pyspark)
- [Towards Data Science](https://towardsdatascience.com/)

## 🎓 Resume Impact

This project demonstrates **Business Analyst Level 1** competencies:

### Technical Competencies
- ✅ **SQL**: Advanced queries, optimization, data modeling
- ✅ **Python**: Data analysis, ML, automation
- ✅ **PySpark**: Big data processing, distributed computing
- ✅ **Power BI**: Dashboard creation, DAX, visualization
- ✅ **Machine Learning**: Predictive modeling, clustering

### Business Competencies
- ✅ **Data Analysis**: Customer insights, performance metrics
- ✅ **Business Intelligence**: KPI development, reporting
- ✅ **Predictive Analytics**: Forecasting, trend analysis
- ✅ **Stakeholder Communication**: Dashboard creation, insights presentation
- ✅ **Strategic Thinking**: Data-driven decision making

### Project Management
- ✅ **End-to-End Delivery**: Complete analytics pipeline
- ✅ **Documentation**: Comprehensive guides and instructions
- ✅ **Code Quality**: Clean, maintainable, well-documented code
- ✅ **Scalability**: Production-ready architecture

## 🚀 Next Steps

### Immediate Actions
1. **Run the project** to understand the workflow
2. **Customize analysis** for your specific needs
3. **Create Power BI dashboards** for stakeholders
4. **Document insights** and recommendations

### Future Enhancements
1. **Real-time Data**: Connect to live data sources
2. **Advanced ML**: Deep learning models, NLP analysis
3. **Automation**: Scheduled reports, alerts
4. **Integration**: Connect with other business systems
5. **Scalability**: Cloud deployment, larger datasets

### Career Development
1. **Portfolio**: Add this project to your portfolio
2. **Interview Prep**: Use as talking points for technical interviews
3. **Skill Building**: Expand on areas of interest
4. **Networking**: Share insights with the analytics community

---

## 📞 Support & Questions

If you have questions or need help with the project:

1. **Check the documentation** in the `docs/` folder
2. **Review the logs** for error messages
3. **Verify your setup** matches the requirements
4. **Customize the code** for your specific needs

## 🎉 Success Metrics

You'll know the project is successful when you can:
- ✅ Run the complete analysis pipeline
- ✅ Create interactive Power BI dashboards
- ✅ Explain the business insights to stakeholders
- ✅ Customize the analysis for different datasets
- ✅ Demonstrate the skills in interviews

**Good luck with your Business Analytics journey! 🚀** 