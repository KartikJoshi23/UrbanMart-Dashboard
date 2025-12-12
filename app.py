"""
UrbanMart Sales Dashboard - Streamlit Application
==================================================
Interactive web-based dashboard for analyzing UrbanMart retail sales data.

Author: MAIB Student
Course: Python Programming with Streamlit

Deployment: Streamlit Cloud via GitHub
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="UrbanMart Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================================================================
# DATA LOADING AND PREPARATION FUNCTIONS
# =============================================================================

@st.cache_data
def load_data():
    """
    Load and prepare the sales data.
    
    Returns:
        pandas.DataFrame: Prepared DataFrame
    """
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, "urbanmart_sales.csv")
    
    df = pd.read_csv(filepath)
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Create derived columns
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.strftime('%Y-%m')
    
    return df


def filter_data(df, start_date, end_date, stores, channel, categories):
    """
    Filter DataFrame based on sidebar selections.
    
    Args:
        df (pandas.DataFrame): Original DataFrame
        start_date: Start date
        end_date: End date
        stores (list): Selected store locations
        channel (str): Selected channel
        categories (list): Selected product categories
        
    Returns:
        pandas.DataFrame: Filtered DataFrame
    """
    filtered_df = df.copy()
    
    # Filter by date range
    filtered_df = filtered_df[
        (filtered_df['date'] >= pd.to_datetime(start_date)) &
        (filtered_df['date'] <= pd.to_datetime(end_date))
    ]
    
    # Filter by stores
    if stores:
        filtered_df = filtered_df[filtered_df['store_location'].isin(stores)]
    
    # Filter by channel
    if channel != 'All':
        filtered_df = filtered_df[filtered_df['channel'] == channel]
    
    # Filter by categories
    if categories:
        filtered_df = filtered_df[filtered_df['product_category'].isin(categories)]
    
    return filtered_df


# =============================================================================
# KPI CALCULATION FUNCTIONS
# =============================================================================

def compute_total_revenue(df):
    """Calculate total revenue."""
    return df['line_revenue'].sum()


def compute_total_transactions(df):
    """Calculate total number of transactions."""
    return df['transaction_id'].nunique()


def compute_avg_revenue_per_transaction(df):
    """Calculate average revenue per transaction."""
    total_revenue = df['line_revenue'].sum()
    total_bills = df['bill_id'].nunique()
    if total_bills > 0:
        return total_revenue / total_bills
    return 0


def compute_unique_customers(df):
    """Calculate number of unique customers."""
    return df['customer_id'].nunique()


def get_revenue_by_category(df):
    """Get revenue breakdown by product category."""
    return df.groupby('product_category')['line_revenue'].sum().sort_values(ascending=True)


def get_revenue_by_store(df):
    """Get revenue breakdown by store location."""
    return df.groupby('store_location')['line_revenue'].sum().sort_values(ascending=True)


def get_daily_revenue(df):
    """Get daily revenue trend."""
    return df.groupby('date')['line_revenue'].sum().reset_index()


def get_top_products(df, n=5):
    """Get top N products by revenue."""
    return df.groupby('product_name')['line_revenue'].sum().sort_values(ascending=False).head(n).reset_index()


def get_top_customers(df, n=5):
    """Get top N customers by revenue."""
    return df.groupby('customer_id')['line_revenue'].sum().sort_values(ascending=False).head(n).reset_index()


def get_revenue_by_channel(df):
    """Get revenue breakdown by channel."""
    return df.groupby('channel')['line_revenue'].sum()


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main function to run the Streamlit dashboard."""
    
    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------
    
    st.title("🛒 UrbanMart Sales Dashboard")
    st.markdown("**Built by MAIB students using Python & Streamlit**")
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # LOAD DATA
    # -------------------------------------------------------------------------
    
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("❌ Error: 'urbanmart_sales.csv' file not found.")
        st.info("Please ensure the data file is in the repository.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()
    
    # -------------------------------------------------------------------------
    # SIDEBAR FILTERS
    # -------------------------------------------------------------------------
    
    st.sidebar.header("🔍 Filters")
    st.sidebar.markdown("Use the filters below to explore the data.")
    
    # Date range filter
    st.sidebar.subheader("📅 Date Range")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select date range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Handle single date selection
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]
    
    # Store location filter
    st.sidebar.subheader("🏪 Store Location")
    all_stores = df['store_location'].unique().tolist()
    selected_stores = st.sidebar.multiselect(
        "Select store locations:",
        options=all_stores,
        default=all_stores
    )
    
    # Channel filter
    st.sidebar.subheader("📱 Sales Channel")
    channel_options = ['All', 'In-store', 'Online']
    selected_channel = st.sidebar.selectbox(
        "Select channel:",
        options=channel_options
    )
    
    # Product category filter
    st.sidebar.subheader("📦 Product Category")
    all_categories = df['product_category'].unique().tolist()
    selected_categories = st.sidebar.multiselect(
        "Select categories:",
        options=all_categories,
        default=all_categories
    )
    
    # Sidebar footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 About")
    st.sidebar.info(
        "This dashboard analyzes UrbanMart's retail sales data. "
        "Use the filters above to explore different segments of the data."
    )
    
    # -------------------------------------------------------------------------
    # APPLY FILTERS
    # -------------------------------------------------------------------------
    
    df_filtered = filter_data(
        df,
        start_date,
        end_date,
        selected_stores,
        selected_channel,
        selected_categories
    )
    
    # Check if filtered data is empty
    if df_filtered.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust your filter criteria.")
        st.stop()
    
    # -------------------------------------------------------------------------
    # KEY METRICS
    # -------------------------------------------------------------------------
    
    st.header("📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = compute_total_revenue(df_filtered)
        st.metric(
            label="💰 Total Revenue",
            value=f"${total_revenue:,.2f}"
        )
    
    with col2:
        total_transactions = compute_total_transactions(df_filtered)
        st.metric(
            label="🧾 Total Transactions",
            value=f"{total_transactions:,}"
        )
    
    with col3:
        avg_revenue = compute_avg_revenue_per_transaction(df_filtered)
        st.metric(
            label="📈 Avg Revenue/Bill",
            value=f"${avg_revenue:,.2f}"
        )
    
    with col4:
        unique_customers = compute_unique_customers(df_filtered)
        st.metric(
            label="👥 Unique Customers",
            value=f"{unique_customers:,}"
        )
    
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # CHARTS ROW 1: Revenue by Category and Store
    # -------------------------------------------------------------------------
    
    st.header("📈 Revenue Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue by Product Category")
        revenue_by_category = get_revenue_by_category(df_filtered)
        
        fig_category = px.bar(
            x=revenue_by_category.values,
            y=revenue_by_category.index,
            orientation='h',
            labels={'x': 'Revenue ($)', 'y': 'Category'},
            color=revenue_by_category.values,
            color_continuous_scale='Blues'
        )
        fig_category.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            height=400
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        st.subheader("Revenue by Store Location")
        revenue_by_store = get_revenue_by_store(df_filtered)
        
        fig_store = px.bar(
            x=revenue_by_store.values,
            y=revenue_by_store.index,
            orientation='h',
            labels={'x': 'Revenue ($)', 'y': 'Store Location'},
            color=revenue_by_store.values,
            color_continuous_scale='Greens'
        )
        fig_store.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            height=400
        )
        st.plotly_chart(fig_store, use_container_width=True)
    
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # CHARTS ROW 2: Daily Trend and Channel Distribution
    # -------------------------------------------------------------------------
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📅 Daily Revenue Trend")
        daily_revenue = get_daily_revenue(df_filtered)
        
        fig_trend = px.line(
            daily_revenue,
            x='date',
            y='line_revenue',
            labels={'date': 'Date', 'line_revenue': 'Revenue ($)'},
            markers=True
        )
        fig_trend.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Revenue ($)"
        )
        fig_trend.update_traces(line_color='#1f77b4', marker_color='#1f77b4')
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        st.subheader("📱 Revenue by Channel")
        revenue_by_channel = get_revenue_by_channel(df_filtered)
        
        fig_channel = px.pie(
            values=revenue_by_channel.values,
            names=revenue_by_channel.index,
            color_discrete_sequence=['#2ecc71', '#3498db']
        )
        fig_channel.update_layout(height=400)
        fig_channel.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_channel, use_container_width=True)
    
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # TABLES: Top Products and Top Customers
    # -------------------------------------------------------------------------
    
    st.header("🏆 Top Performers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 5 Products by Revenue")
        top_products = get_top_products(df_filtered, n=5)
        top_products.columns = ['Product Name', 'Revenue ($)']
        top_products['Revenue ($)'] = top_products['Revenue ($)'].apply(lambda x: f"${x:,.2f}")
        top_products.index = range(1, len(top_products) + 1)
        st.table(top_products)
    
    with col2:
        st.subheader("Top 5 Customers by Revenue")
        top_customers = get_top_customers(df_filtered, n=5)
        top_customers.columns = ['Customer ID', 'Revenue ($)']
        top_customers['Revenue ($)'] = top_customers['Revenue ($)'].apply(lambda x: f"${x:,.2f}")
        top_customers.index = range(1, len(top_customers) + 1)
        st.table(top_customers)
    
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # ADDITIONAL INSIGHTS
    # -------------------------------------------------------------------------
    
    st.header("📋 Additional Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Payment Methods")
        payment_dist = df_filtered.groupby('payment_method')['line_revenue'].sum()
        fig_payment = px.pie(
            values=payment_dist.values,
            names=payment_dist.index,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_payment.update_traces(textposition='inside', textinfo='percent+label')
        fig_payment.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_payment, use_container_width=True)
    
    with col2:
        st.subheader("Customer Segments")
        segment_dist = df_filtered.groupby('customer_segment')['line_revenue'].sum()
        fig_segment = px.pie(
            values=segment_dist.values,
            names=segment_dist.index,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_segment.update_traces(textposition='inside', textinfo='percent+label')
        fig_segment.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_segment, use_container_width=True)
    
    with col3:
        st.subheader("Revenue by Day of Week")
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_revenue = df_filtered.groupby('day_of_week')['line_revenue'].sum().reindex(day_order).dropna()
        
        if not day_revenue.empty:
            fig_day = px.bar(
                x=day_revenue.index,
                y=day_revenue.values,
                labels={'x': 'Day', 'y': 'Revenue ($)'},
                color=day_revenue.values,
                color_continuous_scale='Oranges'
            )
            fig_day.update_layout(
                height=300,
                showlegend=False,
                coloraxis_showscale=False,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_day, use_container_width=True)
        else:
            st.info("No data available for day of week analysis.")
    
    st.markdown("---")
    
    # -------------------------------------------------------------------------
    # RAW DATA PREVIEW
    # -------------------------------------------------------------------------
    
    st.header("📄 Raw Data Preview")
    
    with st.expander("Click to view filtered data (first 20 rows)"):
        display_columns = [
            'transaction_id', 'date', 'store_location', 'customer_id',
            'product_name', 'product_category', 'quantity', 'unit_price',
            'discount_applied', 'line_revenue', 'channel', 'payment_method'
        ]
        st.dataframe(
            df_filtered[display_columns].head(20),
            use_container_width=True
        )
    
    # -------------------------------------------------------------------------
    # DOWNLOAD OPTION
    # -------------------------------------------------------------------------
    
    st.subheader("📥 Download Filtered Data")
    
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="urbanmart_filtered_data.csv",
        mime="text/csv"
    )
    
    # -------------------------------------------------------------------------
    # FOOTER
    # -------------------------------------------------------------------------
    
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>UrbanMart Sales Dashboard | Built with Python & Streamlit</p>
            <p>© 2025 MAIB Student Project</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =============================================================================
# RUN APPLICATION
# =============================================================================

if __name__ == "__main__":
    main()
