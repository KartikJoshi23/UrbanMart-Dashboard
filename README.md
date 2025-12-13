# UrbanMart Sales Dashboard

An interactive sales analytics dashboard built with Python and Streamlit.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Live Demo](#live-demo)
3. [Features](#features)
4. [Dataset Description](#dataset-description)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Project Structure](#project-structure)
8. [Analysis Questions](#analysis-questions)
9. [Question 1](#question-1)
10. [Question 2](#question-2)
11. [Question 3](#question-3)
12. [Question 4](#question-4)
13. [Question 5](#question-5)
14. [Technologies Used](#technologies-used)
15. [Author](#author)

---

## Project Overview

UrbanMart is a retail analytics project that demonstrates data analysis and visualization skills using Python. The project analyzes sales transactions from a fictional retail chain to derive actionable business insights.

Key Objectives:
- Analyze sales trends over time
- Compare store performance across locations
- Identify top-performing products and categories
- Understand customer purchasing behavior
- Build an interactive dashboard for data exploration

---

## Live Demo

View the live dashboard here: https://urbanmart-dashboard.streamlit.app/

Replace with your actual Streamlit Cloud URL after deployment.

---

## Features

- Interactive KPI Cards showing real-time metrics
- Monthly and daily revenue trend analysis
- Store performance comparison across locations
- Product category breakdown with revenue share
- Customer segment analysis
- Payment method distribution
- Dynamic filters for date, store, category, and segment
- Data export functionality

---

## Dataset Description

The dataset contains retail transaction records.

| Column | Description |
|--------|-------------|
| transaction_id | Unique transaction identifier |
| bill_id | Bill number |
| date | Transaction date |
| store_id | Store identifier |
| store_location | Store location name |
| customer_id | Customer identifier |
| customer_segment | Loyal, Regular, or New |
| product_id | Product identifier |
| product_category | Product category |
| product_name | Product name |
| quantity | Units purchased |
| unit_price | Price per unit |
| payment_method | Cash, Credit Card, UPI, Debit Card |
| discount_applied | Discount amount |
| channel | In-store or Online |

Dataset Statistics:
- Records: 250 transactions
- Time Period: January to March 2025
- Stores: 3 locations
- Categories: 6 product categories

---

## Installation

Prerequisites:
- Python 3.8 or higher
- pip package manager

Steps:

Step 1: Clone the repository using git clone command

Step 2: Navigate to the project folder

Step 3: Install dependencies using: pip install -r requirements.txt

Step 4: Run the dashboard using: streamlit run app.py

Step 5: Open browser at http://localhost:8501

---

## Usage

Running Locally: Use the command streamlit run app.py

Using Filters:
- Date Range: Select start and end dates
- Store Location: Choose one or multiple stores
- Sales Channel: Filter by In-store or Online
- Product Category: Select specific categories
- Customer Segment: Filter by customer type

Exporting Data: Click the Download button to export filtered data as CSV.

---

## Project Structure

The repository contains the following files:

- app.py: Main Streamlit dashboard application
- urbanmart_sales.csv: Sales dataset with transaction records
- requirements.txt: Python package dependencies
- README.md: Project documentation

---

## Analysis Questions

This section covers the five business questions analyzed in this project.

---

## Question 1

Topic: Monthly Revenue Trend

Question: How does revenue change month over month?

Analysis: Calculated total revenue for each month and created visualizations to identify trends.

Key Findings:
- January showed strong sales due to New Year period
- Revenue remained stable across Q1
- Weekend sales consistently outperformed weekdays

---

## Question 2

Topic: Store Performance

Question: Which store location generates the highest revenue?

Analysis: Aggregated revenue by store location and compared metrics.

Key Findings:
- Downtown store leads in total revenue
- Suburban store has highest transaction volume
- Uptown store shows highest average bill value

---

## Question 3

Topic: Product Category Analysis

Question: Which product categories contribute most to revenue?

Analysis: Grouped sales by product category and calculated revenue shares.

Key Findings:
- Grocery category leads with highest revenue
- Beverages show consistent demand
- Personal Care products have good margins

---

## Question 4

Topic: Customer Segment Analysis

Question: How do different customer segments contribute to sales?

Analysis: Segmented customers and compared spending patterns.

Key Findings:
- Loyal customers contribute 45 percent of revenue
- New customers show high average basket value
- Regular customers visit most frequently

---

## Question 5

Topic: Payment Method Distribution

Question: What are the preferred payment methods?

Analysis: Counted transactions by payment method and calculated revenue share.

Key Findings:
- Credit Card is most popular at 40 percent of transactions
- UPI dominates online channel
- Cash preferred for smaller transactions

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Programming language |
| Pandas | Data manipulation |
| Streamlit | Dashboard framework |
| Plotly | Visualizations |
| GitHub | Version control |
| Streamlit Cloud | Deployment |

---

## Author

Kartik Joshi

MAIB Student

GitHub: https://github.com/yourusername

---

## License

This project is licensed under the MIT License.
