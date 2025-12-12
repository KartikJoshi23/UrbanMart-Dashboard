# 🛒 UrbanMart Sales Dashboard

An interactive sales analytics dashboard built with Python and Streamlit for analyzing retail sales data.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Live Demo](#live-demo)
- [Features](#features)
- [Dataset Description](#dataset-description)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Analysis Questions](#analysis-questions)
  - [Question 1 Monthly Revenue Trend](#question-1-monthly-revenue-trend)
  - [Question 2 Store Performance](#question-2-store-performance)
  - [Question 3 Product Category Analysis](#question-3-product-category-analysis)
  - [Question 4 Customer Segment Analysis](#question-4-customer-segment-analysis)
  - [Question 5 Payment Method Distribution](#question-5-payment-method-distribution)
- [Technologies Used](#technologies-used)
- [Screenshots](#screenshots)
- [Author](#author)

---

## Project Overview

UrbanMart is a retail analytics project that demonstrates data analysis and visualization skills using Python. The project analyzes sales transactions from a fictional retail chain to derive actionable business insights.

**Key Objectives:**
- Analyze sales trends over time
- Compare store performance across locations
- Identify top-performing products and categories
- Understand customer purchasing behavior
- Build an interactive dashboard for data exploration

---

## Live Demo

🔗 **[View Live Dashboard](https://urbanmart-dashboard.streamlit.app/)**

*(Replace with your actual Streamlit Cloud URL)*

---

## Features

- 📊 **Interactive KPI Cards** - Real-time metrics display
- 📈 **Trend Analysis** - Monthly and daily revenue trends
- 🏪 **Store Comparison** - Performance across locations
- 📦 **Category Breakdown** - Revenue by product category
- 👥 **Customer Insights** - Segment-wise analysis
- 💳 **Payment Analysis** - Payment method distribution
- 🔍 **Dynamic Filters** - Filter by date, store, category, and more
- 📥 **Data Export** - Download filtered data as CSV

---

## Dataset Description

The dataset contains retail transaction records with the following structure:

| Column | Description | Example |
|--------|-------------|---------|
| `transaction_id` | Unique transaction identifier | TXN-2025-0001 |
| `bill_id` | Bill/invoice number | BILL-0001 |
| `date` | Transaction date | 2025-01-15 |
| `store_id` | Store identifier | S1 |
| `store_location` | Store location name | Downtown |
| `customer_id` | Customer identifier | C001 |
| `customer_segment` | Customer type | Loyal, Regular, New |
| `product_id` | Product identifier | P101 |
| `product_category` | Product category | Beverages, Snacks, etc. |
| `product_name` | Product name | Orange Juice 1L |
| `quantity` | Units purchased | 2 |
| `unit_price` | Price per unit | 3.50 |
| `payment_method` | Payment type | Cash, Credit Card, UPI |
| `discount_applied` | Discount amount | 0.50 |
| `channel` | Sales channel | In-store, Online |

**Dataset Statistics:**
- **Records:** 250+ transactions
- **Time Period:** January - March 2025
- **Stores:** 3 locations
- **Categories:** 6 product categories

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/urbanmart-dashboard.git
cd urbanmart-dashboard
