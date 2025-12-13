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
- Records: 250+ transactions
- Time Period: January to March 2025
- Stores: 3 locations
- Categories: 6 product categories

---

## Installation

Prerequisites:
- Python 3.8 or higher
- pip package manager

Steps:

1. Clone the repository
