"""
UrbanMart Sales Dashboard - Streamlit Application
==================================================
Interactive web-based dashboard for analyzing UrbanMart retail sales data.
Features full-year analysis with quarterly, monthly, and daily trends.

Author: MAIB Student
Course: Python Programming with Streamlit
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
# CUSTOM CSS
# =============================================================================

st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .stMetric {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


# =============================================================================
# DATA LOADING AND PREPARATION
# =============================================================================

@st.cache_data
def load_data():
    """Load and prepare the sales data."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, "urbanmart_sales.csv")
    
    df = pd.read_csv(filepath)
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Create derived columns
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.to_period('M').astype(str)
    df['month_name'] = df['date'].dt.strftime('%B')
    df['quarter'] = df['date'].dt.to_period('Q').astype(str)
    df['year_month'] = df['date'].dt.strftime('%Y-%m')
    df['week'] = df['date'].dt.isocalendar().week
    df['year'] = df['date'].dt.year
    
    return df


def filter_data(df, start_date, end_date, stores, channel, categories, segments, quarters):
    """Filter DataFrame based on sidebar selections."""
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
    
    # Filter by customer segments
    if segments:
        filtered_df = filtered_df[filtered_df['customer_segment'].isin(segments)]
    
    # Filter by quarters
    if quarters:
        filtered_df = filtered_df[filtered_df['quarter'].isin(quarters)]
    
    return filtered_df


# =============================================================================
# KPI CALCULATION FUNCTIONS
# =============================================================================

def compute_kpis(df):
    """Calculate all KPIs."""
    return {
        'total_revenue': df['line_revenue'].sum(),
        'total_transactions': df['transaction_id'].nunique(),
        'total_bills': df['bill_id'].nunique(),
        'avg_revenue_per_bill': df.groupby('bill_id')['line_revenue'].sum().mean() if df['bill_id'].nunique() > 0 else 0,
        'unique_customers': df['customer_id'].nunique(),
        'total_units_sold': df['quantity'].sum(),
        'avg_discount': df['discount_applied'].mean(),
        'total_discount': df['discount_applied'].sum()
    }


def calculate_growth(current, previous):
    """Calculate percentage growth."""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100


# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================

def create_monthly_trend_chart(df):
    """Create monthly revenue trend chart."""
    monthly_data = df.groupby('year_month').agg({
        'line_revenue': 'sum',
        'transaction_id': 'nunique'
    }).reset_index()
    monthly_data.columns = ['Month', 'Revenue', 'Transactions']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_data['Month'],
        y=monthly_data['Revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Monthly Revenue Trend',
        xaxis_title='Month',
        yaxis_title='Revenue ($)',
        hovermode='x unified',
        height=400
    )
    
    return fig


def create_quarterly_comparison_chart(df):
    """Create quarterly comparison chart."""
    quarterly_data = df.groupby('quarter')['line_revenue'].sum().reset_index()
    quarterly_data.columns = ['Quarter', 'Revenue']
    
    fig = px.bar(
        quarterly_data,
        x='Quarter',
        y='Revenue',
        color='Revenue',
        color_continuous_scale='Blues',
        title='Quarterly Revenue Comparison'
    )
    
    fig.update_layout(
        xaxis_title='Quarter',
        yaxis_title='Revenue ($)',
        showlegend=False,
        coloraxis_showscale=False,
        height=400
    )
    
    return fig


def create_category_revenue_chart(df):
    """Create revenue by category chart."""
    category_data = df.groupby('product_category')['line_revenue'].sum().sort_values(ascending=True)
    
    fig = px.bar(
        x=category_data.values,
        y=category_data.index,
        orientation='h',
        color=category_data.values,
        color_continuous_scale='Viridis',
        title='Revenue by Product Category'
    )
    
    fig.update_layout(
        xaxis_title='Revenue ($)',
        yaxis_title='Category',
        showlegend=False,
        coloraxis_showscale=False,
        height=400
    )
    
    return fig


def create_store_revenue_chart(df):
    """Create revenue by store chart."""
    store_data = df.groupby('store_location')['line_revenue'].sum().sort_values(ascending=True)
    
    fig = px.bar(
        x=store_data.values,
        y=store_data.index,
        orientation='h',
        color=store_data.values,
        color_continuous_scale='Greens',
        title='Revenue by Store Location'
    )
    
    fig.update_layout(
        xaxis_title='Revenue ($)',
        yaxis_title='Store Location',
        showlegend=False,
        coloraxis_showscale=False,
        height=400
    )
    
    return fig


def create_daily_trend_chart(df):
    """Create daily revenue trend chart."""
    daily_data = df.groupby('date')['line_revenue'].sum().reset_index()
    
    fig = px.line(
        daily_data,
        x='date',
        y='line_revenue',
        title='Daily Revenue Trend'
    )
    
    fig.update_traces(line_color='#1f77b4')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Revenue ($)',
        height=400
    )
    
    return fig


def create_channel_pie_chart(df):
    """Create revenue by channel pie chart."""
    channel_data = df.groupby('channel')['line_revenue'].sum()
    
    fig = px.pie(
        values=channel_data.values,
        names=channel_data.index,
        title='Revenue by Channel',
        color_discrete_sequence=['#2ecc71', '#3498db']
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=350, showlegend=False)
    
    return fig


def create_day_of_week_chart(df):
    """Create revenue by day of week chart."""
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_data = df.groupby('day_of_week')['line_revenue'].sum().reindex(day_order)
    
    fig = px.bar(
        x=day_data.index,
        y=day_data.values,
        color=day_data.values,
        color_continuous_scale='Oranges',
        title='Revenue by Day of Week'
    )
    
    fig.update_layout(
        xaxis_title='Day',
        yaxis_title='Revenue ($)',
        showlegend=False,
        coloraxis_showscale=False,
        height=350,
        xaxis_tickangle=-45
    )
    
    return fig


def create_segment_chart(df):
    """Create customer segment distribution chart."""
    segment_data = df.groupby('customer_segment')['line_revenue'].sum()
    
    fig = px.pie(
        values=segment_data.values,
        names=segment_data.index,
        title='Revenue by Customer Segment',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=350, showlegend=False)
    
    return fig


def create_payment_chart(df):
    """Create payment method distribution chart."""
    payment_data = df.groupby('payment_method')['line_revenue'].sum()
    
    fig = px.pie(
        values=payment_data.values,
        names=payment_data.index,
        title='Revenue by Payment Method',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=350, showlegend=False)
    
    return fig


def create_monthly_category_heatmap(df):
    """Create monthly category revenue heatmap."""
    pivot_data = df.pivot_table(
        values='line_revenue',
        index='product_category',
        columns='year_month',
        aggfunc='sum',
        fill_value=0
    )
    
    fig = px.imshow(
        pivot_data,
        labels=dict(x="Month", y="Category", color="Revenue"),
        aspect="auto",
        color_continuous_scale='Blues',
        title='Monthly Revenue by Category (Heatmap)'
    )
    
    fig.update_layout(height=400)
    
    return fig


def create_store_monthly_trend(df):
    """Create store-wise monthly trend."""
    store_monthly = df.groupby(['year_month', 'store_location'])['line_revenue'].sum().reset_index()
    
    fig = px.line(
        store_monthly,
        x='year_month',
        y='line_revenue',
        color='store_location',
        title='Monthly Revenue Trend by Store',
        markers=True
    )
    
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Revenue ($)',
        legend_title='Store Location',
        height=400
    )
    
    return fig


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main function to run the Streamlit dashboard."""
    
    # =========================================================================
    # HEADER
    # =========================================================================
    
    st.title("🛒 UrbanMart Sales Dashboard")
    st.markdown("**Full-Year Analytics Dashboard | Built with Python & Streamlit**")
    st.markdown("---")
    
    # =========================================================================
    # LOAD DATA
    # =========================================================================
    
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("❌ Error: 'urbanmart_sales.csv' file not found.")
        st.info("Please run `python generate_dataset.py` first to create the dataset.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()
    
    # =========================================================================
    # SIDEBAR FILTERS
    # =========================================================================
    
    st.sidebar.header("🔍 Filters")
    
    # Date Range
    st.sidebar.subheader("📅 Date Range")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select date range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]
    
    # Quarter Filter
    st.sidebar.subheader("📊 Quarter")
    all_quarters = sorted(df['quarter'].unique().tolist())
    selected_quarters = st.sidebar.multiselect(
        "Select quarters:",
        options=all_quarters,
        default=all_quarters
    )
    
    # Store Location
    st.sidebar.subheader("🏪 Store Location")
    all_stores = df['store_location'].unique().tolist()
    selected_stores = st.sidebar.multiselect(
        "Select store locations:",
        options=all_stores,
        default=all_stores
    )
    
    # Channel
    st.sidebar.subheader("📱 Sales Channel")
    channel_options = ['All', 'In-store', 'Online']
    selected_channel = st.sidebar.selectbox(
        "Select channel:",
        options=channel_options
    )
    
    # Product Category
    st.sidebar.subheader("📦 Product Category")
    all_categories = df['product_category'].unique().tolist()
    selected_categories = st.sidebar.multiselect(
        "Select categories:",
        options=all_categories,
        default=all_categories
    )
    
    # Customer Segment
    st.sidebar.subheader("👥 Customer Segment")
    all_segments = df['customer_segment'].unique().tolist()
    selected_segments = st.sidebar.multiselect(
        "Select segments:",
        options=all_segments,
        default=all_segments
    )
    
    # Sidebar Info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 About")
    st.sidebar.info(
        "This dashboard provides full-year analytics for UrbanMart retail sales. "
        "Use filters to explore trends by quarter, month, store, and more."
    )
    
    # =========================================================================
    # APPLY FILTERS
    # =========================================================================
    
    df_filtered = filter_data(
        df, start_date, end_date, selected_stores, 
        selected_channel, selected_categories, selected_segments, selected_quarters
    )
    
    if df_filtered.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust your criteria.")
        st.stop()
    
    # =========================================================================
    # KEY METRICS
    # =========================================================================
    
    st.header("📊 Key Performance Indicators")
    
    kpis = compute_kpis(df_filtered)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=f"${kpis['total_revenue']:,.2f}"
        )
    
    with col2:
        st.metric(
            label="🧾 Total Bills",
            value=f"{kpis['total_bills']:,}"
        )
    
    with col3:
        st.metric(
            label="📈 Avg Revenue/Bill",
            value=f"${kpis['avg_revenue_per_bill']:,.2f}"
        )
    
    with col4:
        st.metric(
            label="👥 Unique Customers",
            value=f"{kpis['unique_customers']:,}"
        )
    
    # Second row of metrics
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="📦 Total Units Sold",
            value=f"{kpis['total_units_sold']:,}"
        )
    
    with col6:
        st.metric(
            label="🏷️ Total Discounts",
            value=f"${kpis['total_discount']:,.2f}"
        )
    
    with col7:
        st.metric(
            label="📊 Total Transactions",
            value=f"{kpis['total_transactions']:,}"
        )
    
    with col8:
        st.metric(
            label="💵 Avg Discount/Item",
            value=f"${kpis['avg_discount']:,.2f}"
        )
    
    st.markdown("---")
    
    # =========================================================================
    # TREND ANALYSIS SECTION
    # =========================================================================
    
    st.header("📈 Trend Analysis")
    
    tab1, tab2, tab3 = st.tabs(["📅 Monthly Trends", "📊 Quarterly Analysis", "📆 Daily Patterns"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_monthly_trend_chart(df_filtered), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_store_monthly_trend(df_filtered), use_container_width=True)
        
        st.plotly_chart(create_monthly_category_heatmap(df_filtered), use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_quarterly_comparison_chart(df_filtered), use_container_width=True)
        
        with col2:
            # Quarterly metrics table
            st.subheader("Quarterly Summary")
            quarterly_summary = df_filtered.groupby('quarter').agg({
                'line_revenue': 'sum',
                'bill_id': 'nunique',
                'customer_id': 'nunique',
                'quantity': 'sum'
            }).reset_index()
            quarterly_summary.columns = ['Quarter', 'Revenue', 'Bills', 'Customers', 'Units Sold']
            quarterly_summary['Revenue'] = quarterly_summary['Revenue'].apply(lambda x: f"${x:,.2f}")
            quarterly_summary['Bills'] = quarterly_summary['Bills'].apply(lambda x: f"{x:,}")
            quarterly_summary['Customers'] = quarterly_summary['Customers'].apply(lambda x: f"{x:,}")
            quarterly_summary['Units Sold'] = quarterly_summary['Units Sold'].apply(lambda x: f"{x:,}")
            st.dataframe(quarterly_summary, use_container_width=True, hide_index=True)
    
    with tab3:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.plotly_chart(create_daily_trend_chart(df_filtered), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_day_of_week_chart(df_filtered), use_container_width=True)
    
    st.markdown("---")
    
    # =========================================================================
    # REVENUE ANALYSIS
    # =========================================================================
    
    st.header("💰 Revenue Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_category_revenue_chart(df_filtered), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_store_revenue_chart(df_filtered), use_container_width=True)
    
    st.markdown("---")
    
    # =========================================================================
    # CUSTOMER & CHANNEL INSIGHTS
    # =========================================================================
    
    st.header("👥 Customer & Channel Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.plotly_chart(create_channel_pie_chart(df_filtered), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_segment_chart(df_filtered), use_container_width=True)
    
    with col3:
        st.plotly_chart(create_payment_chart(df_filtered), use_container_width=True)
    
    st.markdown("---")
    
    # =========================================================================
    # TOP PERFORMERS
    # =========================================================================
    
    st.header("🏆 Top Performers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Products by Revenue")
        top_products = df_filtered.groupby('product_name')['line_revenue'].sum().sort_values(ascending=False).head(10).reset_index()
        top_products.columns = ['Product Name', 'Revenue']
        top_products['Revenue'] = top_products['Revenue'].apply(lambda x: f"${x:,.2f}")
        top_products.index = range(1, len(top_products) + 1)
        st.dataframe(top_products, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Customers by Revenue")
        top_customers = df_filtered.groupby('customer_id').agg({
            'line_revenue': 'sum',
            'customer_segment': 'first'
        }).sort_values('line_revenue', ascending=False).head(10).reset_index()
        top_customers.columns = ['Customer ID', 'Revenue', 'Segment']
        top_customers['Revenue'] = top_customers['Revenue'].apply(lambda x: f"${x:,.2f}")
        top_customers.index = range(1, len(top_customers) + 1)
        st.dataframe(top_customers, use_container_width=True)
    
    st.markdown("---")
    
    # =========================================================================
    # STORE ANALYSIS (New Store Highlight)
    # =========================================================================
    
    st.header("🏪 Store Performance Analysis")
    
    # Check if Midtown store data exists
    if 'Midtown' in df_filtered['store_location'].values:
        st.info("📢 **Note:** Midtown store (S4) opened in July 2025. Performance shown from opening date.")
    
    store_metrics = df_filtered.groupby('store_location').agg({
        'line_revenue': 'sum',
        'bill_id': 'nunique',
        'customer_id': 'nunique',
        'quantity': 'sum',
        'discount_applied': 'sum'
    }).reset_index()
    
    store_metrics.columns = ['Store', 'Revenue', 'Bills', 'Customers', 'Units Sold', 'Discounts']
    store_metrics['Avg Revenue/Bill'] = store_metrics['Revenue'] / store_metrics['Bills']
    store_metrics = store_metrics.sort_values('Revenue', ascending=False)
    
    # Format for display
    display_metrics = store_metrics.copy()
    display_metrics['Revenue'] = display_metrics['Revenue'].apply(lambda x: f"${x:,.2f}")
    display_metrics['Avg Revenue/Bill'] = display_metrics['Avg Revenue/Bill'].apply(lambda x: f"${x:,.2f}")
    display_metrics['Discounts'] = display_metrics['Discounts'].apply(lambda x: f"${x:,.2f}")
    display_metrics['Bills'] = display_metrics['Bills'].apply(lambda x: f"{x:,}")
    display_metrics['Customers'] = display_metrics['Customers'].apply(lambda x: f"{x:,}")
    display_metrics['Units Sold'] = display_metrics['Units Sold'].apply(lambda x: f"{x:,}")
    
    st.dataframe(display_metrics, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # =========================================================================
    # RAW DATA PREVIEW
    # =========================================================================
    
    st.header("📄 Data Preview")
    
    with st.expander("Click to view filtered data (first 50 rows)"):
        display_columns = [
            'transaction_id', 'date', 'store_location', 'customer_id', 'customer_segment',
            'product_name', 'product_category', 'quantity', 'unit_price',
            'discount_applied', 'line_revenue', 'channel', 'payment_method'
        ]
        st.dataframe(df_filtered[display_columns].head(50), use_container_width=True)
    
    # =========================================================================
    # DOWNLOAD SECTION
    # =========================================================================
    
    st.subheader("📥 Download Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_filtered = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Data (CSV)",
            data=csv_filtered,
            file_name="urbanmart_filtered_data.csv",
            mime="text/csv"
        )
    
    with col2:
        # Create summary report
        summary_data = {
            'Metric': ['Total Revenue', 'Total Bills', 'Unique Customers', 'Total Units Sold', 'Total Discounts'],
            'Value': [
                f"${kpis['total_revenue']:,.2f}",
                f"{kpis['total_bills']:,}",
                f"{kpis['unique_customers']:,}",
                f"{kpis['total_units_sold']:,}",
                f"${kpis['total_discount']:,.2f}"
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_csv = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Summary Report (CSV)",
            data=summary_csv,
            file_name="urbanmart_summary_report.csv",
            mime="text/csv"
        )
    
    # =========================================================================
    # FOOTER
    # =========================================================================
    
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>🛒 UrbanMart Sales Dashboard | Full-Year Analytics</p>
            <p>Built with Python & Streamlit | © 2025 MAIB Student Project</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =============================================================================
# RUN APPLICATION
# =============================================================================

if __name__ == "__main__":
    main()
