# 🛒 UrbanMart Sales Dashboard

An interactive retail analytics dashboard built with Python and Streamlit featuring **full-year sales analysis** with quarterly, monthly, and daily trends.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://urbanmart-dashboard.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Dataset Description](#-dataset-description)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)
- [Reflection Questions](#-reflection-questions)
- [Author](#-author)

---

## 🎯 Overview

**UrbanMart** is a mid-sized retail chain operating in a metropolitan city. This dashboard provides comprehensive **full-year analytics** (January - December 2025) to help management understand:

- 📈 Quarterly and monthly revenue trends
- 🏪 Store-wise performance comparison
- 📦 Product category analysis
- 👥 Customer segment insights
- 📅 Seasonal and promotional impact

### Business Scenarios Included

| Scenario | Description | Period |
|----------|-------------|--------|
| 🏪 New Store Opening | Midtown store (S4) launch | July 2025 |
| ☀️ Summer Sale | Promotional period with discounts | May 15 - June 30 |
| 🪔 Diwali Sale | Festival promotional period | Oct 15 - Nov 15 |
| 🎄 Christmas Sale | Holiday promotional period | Dec 15 - Dec 31 |

---

## ✨ Features

### 🔍 Advanced Filters
| Filter | Description |
|--------|-------------|
| Date Range | Custom date selection |
| Quarter | Q1, Q2, Q3, Q4 filter |
| Store Location | Downtown, Suburban, Uptown, Midtown |
| Sales Channel | In-store, Online, All |
| Product Category | 6 categories |
| Customer Segment | Loyal, Regular, New |

### 📊 Key Metrics (KPIs)
- Total Revenue
- Total Bills
- Average Revenue per Bill
- Unique Customers
- Total Units Sold
- Total Discounts
- Total Transactions
- Average Discount per Item

### 📈 Visualizations

| Chart Type | Description |
|------------|-------------|
| Monthly Trend Line | Revenue trend across months |
| Quarterly Bar Chart | Q1-Q4 revenue comparison |
| Store Monthly Trend | Store-wise monthly performance |
| Category Heatmap | Monthly revenue by category |
| Daily Pattern | Daily revenue with day-of-week analysis |
| Pie Charts | Channel, Segment, Payment distribution |
| Horizontal Bars | Category and Store revenue |

### 📋 Data Tables
- Top 10 Products by Revenue
- Top 10 Customers by Revenue
- Quarterly Summary
- Store Performance Metrics

---

## 📊 Dataset Description

### Overview
| Attribute | Value |
|-----------|-------|
| **File Name** | `urbanmart_sales.csv` |
| **Total Records** | ~2,000-2,500 transactions |
| **Date Range** | January 1, 2025 - December 31, 2025 |
| **Stores** | 4 (Downtown, Suburban, Uptown, Midtown) |
| **Products** | 100+ unique products |
| **Categories** | 6 (Beverages, Snacks, Personal Care, Dairy, Grocery, Bakery) |

### Seasonal Patterns Included

| Pattern | Description |
|---------|-------------|
| **Monthly Seasonality** | Higher sales in Nov-Dec (holidays), lower in Feb |
| **Day of Week** | Peak on Saturday, lowest on Monday |
| **Salary Pattern** | Higher sales in first week of month |
| **Summer Effect** | Increased beverage sales (Apr-Aug) |
| **Winter Effect** | Increased hot beverages, lotions (Nov-Feb) |
| **Festival Effect** | Higher snacks, sweets during Oct-Nov |

### Column Definitions

| Column | Type | Description |
|--------|------|-------------|
| `transaction_id` | String | Unique transaction identifier |
| `bill_id` | String | Bill number (groups items) |
| `date` | Date | Transaction date |
| `store_id` | String | Store identifier (S1-S4) |
| `store_location` | String | Store area name |
| `customer_id` | String | Customer identifier |
| `customer_segment` | String | Loyal/Regular/New |
| `product_id` | String | Product identifier |
| `product_category` | String | Category name |
| `product_name` | String | Product name |
| `quantity` | Integer | Units purchased |
| `unit_price` | Float | Price per unit |
| `payment_method` | String | Cash/Credit Card/UPI/Debit Card |
| `discount_applied` | Float | Discount amount |
| `channel` | String | In-store/Online |

---

## 📁 Project Structure
