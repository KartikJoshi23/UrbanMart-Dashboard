"""
UrbanMart Sales Dashboard
==========================
Interactive dashboard for Q1-Q2 2025 sales analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
# DATA LOADING
# =============================================================================

@st.cache_data
def load_data():
    """Load and prepare sales data."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, "urbanmart_sales.csv")
    
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    
    # Derived columns
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    df['month'] = df['date'].dt.to_period('M').astype(str)
    df['month_name'] = df['date'].dt.strftime('%B %Y')
    df['day_of_week'] = df['date'].dt.day_name()
    df['week'] = df['date'].dt.isocalendar().week
    
    return df

# =============================================================================
# FILTER FUNCTION
# =============================================================================

def filter_data(df, start_date, end_date, stores, channel, categories, segments):
    """Apply filters to dataframe."""
    filtered = df.copy()
    
    filtered = filtered[
        (filtered['date'] >= pd.to_datetime(start_date)) &
        (filtered['date'] <= pd.to_datetime(end_date))
    ]
    
    if stores:
        filtered = filtered[filtered['store_location'].isin(stores)]
    if channel != 'All':
        filtered = filtered[filtered['channel'] == channel]
    if categories:
        filtered = filtered[filtered['product_category'].isin(categories)]
    if segments:
        filtered = filtered[filtered['customer_segment'].isin(segments)]
    
    return filtered

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    # Header
    st.title("🛒 UrbanMart Sales Dashboard")
    st.markdown("**Q1-Q2 2025 Sales Analysis | Built with Python & Streamlit**")
    st.markdown("---")
    
    # Load data
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("❌ 'urbanmart_sales.csv' not found!")
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
        "Select dates:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]
    
    # Store Filter
    st.sidebar.subheader("🏪 Store Location")
    all_stores = df['store_location'].unique().tolist()
    selected_stores = st.sidebar.multiselect(
        "Select stores:",
        options=all_stores,
        default=all_stores
    )
    
    # Channel Filter
    st.sidebar.subheader("📱 Sales Channel")
    selected_channel = st.sidebar.selectbox(
        "Select channel:",
        options=['All', 'In-store', 'Online']
    )
    
    # Category Filter
    st.sidebar.subheader("📦 Product Category")
    all_categories = df['product_category'].unique().tolist()
    selected_categories = st.sidebar.multiselect(
        "Select categories:",
        options=all_categories,
        default=all_categories
    )
    
    # Segment Filter
    st.sidebar.subheader("👥 Customer Segment")
    all_segments = df['customer_segment'].unique().tolist()
    selected_segments = st.sidebar.multiselect(
        "Select segments:",
        options=all_segments,
        default=all_segments
    )
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 Data: {min_date} to {max_date}")
    
    # =========================================================================
    # APPLY FILTERS
    # =========================================================================
    
    df_filtered = filter_data(
        df, start_date, end_date, selected_stores,
        selected_channel, selected_categories, selected_segments
    )
    
    if df_filtered.empty:
        st.warning("⚠️ No data for selected filters!")
        st.stop()
    
    # =========================================================================
    # KPI METRICS
    # =========================================================================
    
    st.header("📊 Key Performance Indicators")
    
    total_revenue = df_filtered['line_revenue'].sum()
    total_bills = df_filtered['bill_id'].nunique()
    avg_bill_value = total_revenue / total_bills if total_bills > 0 else 0
    unique_customers = df_filtered['customer_id'].nunique()
    total_units = df_filtered['quantity'].sum()
    total_discount = df_filtered['discount_applied'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    with col2:
        st.metric("🧾 Total Bills", f"{total_bills:,}")
    with col3:
        st.metric("📈 Avg Bill Value", f"${avg_bill_value:,.2f}")
    with col4:
        st.metric("👥 Unique Customers", f"{unique_customers:,}")
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("📦 Units Sold", f"{total_units:,}")
    with col6:
        st.metric("🏷️ Total Discounts", f"${total_discount:,.2f}")
    with col7:
        st.metric("📋 Transactions", f"{len(df_filtered):,}")
    with col8:
        avg_discount = total_discount / len(df_filtered) if len(df_filtered) > 0 else 0
        st.metric("💵 Avg Discount", f"${avg_discount:,.2f}")
    
    st.markdown("---")
    
    # =========================================================================
    # TREND ANALYSIS
    # =========================================================================
    
    st.header("📈 Trend Analysis")
    
    tab1, tab2 = st.tabs(["📅 Monthly Trends", "📆 Daily Patterns"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly Revenue Trend
            monthly_data = df_filtered.groupby('month_name')['line_revenue'].sum().reset_index()
            monthly_data.columns = ['Month', 'Revenue']
            
            fig_monthly = px.bar(
                monthly_data,
                x='Month',
                y='Revenue',
                title='Monthly Revenue',
                color='Revenue',
                color_continuous_scale='Blues'
            )
            fig_monthly.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_monthly, use_container_width=True)
        
        with col2:
            # Monthly Transactions
            monthly_txn = df_filtered.groupby('month_name')['bill_id'].nunique().reset_index()
            monthly_txn.columns = ['Month', 'Bills']
            
            fig_txn = px.bar(
                monthly_txn,
                x='Month',
                y='Bills',
                title='Monthly Bills',
                color='Bills',
                color_continuous_scale='Greens'
            )
            fig_txn.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_txn, use_container_width=True)
        
        # Store-wise Monthly Trend
        store_monthly = df_filtered.groupby(['month_name', 'store_location'])['line_revenue'].sum().reset_index()
        
        fig_store_trend = px.line(
            store_monthly,
            x='month_name',
            y='line_revenue',
            color='store_location',
            title='Monthly Revenue by Store',
            markers=True
        )
        fig_store_trend.update_layout(
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            legend_title='Store'
        )
        st.plotly_chart(fig_store_trend, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Daily Trend
            daily_data = df_filtered.groupby('date')['line_revenue'].sum().reset_index()
            
            fig_daily = px.line(
                daily_data,
                x='date',
                y='line_revenue',
                title='Daily Revenue Trend'
            )
            fig_daily.update_traces(line_color='#1f77b4')
            st.plotly_chart(fig_daily, use_container_width=True)
        
        with col2:
            # Day of Week
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_data = df_filtered.groupby('day_of_week')['line_revenue'].sum().reindex(day_order)
            
            fig_dow = px.bar(
                x=day_data.index,
                y=day_data.values,
                title='Revenue by Day of Week',
                color=day_data.values,
                color_continuous_scale='Oranges'
            )
            fig_dow.update_layout(
                xaxis_title='Day',
                yaxis_title='Revenue ($)',
                showlegend=False,
                coloraxis_showscale=False,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_dow, use_container_width=True)
    
    st.markdown("---")
    
    # =========================================================================
    # REVENUE BREAKDOWN
    # =========================================================================
    
    st.header("💰 Revenue Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # By Category
        cat_data = df_filtered.groupby('product_category')['line_revenue'].sum().sort_values(ascending=True)
        
        fig_cat = px.bar(
            x=cat_data.values,
            y=cat_data.index,
            orientation='h',
            title='Revenue by Category',
            color=cat_data.values,
            color_continuous_scale='Viridis'
        )
        fig_cat.update_layout(
            xaxis_title='Revenue ($)',
            yaxis_title='Category',
            showlegend=False,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with col2:
        # By Store
        store_data = df_filtered.groupby('store_location')['line_revenue'].sum().sort_values(ascending=True)
        
        fig_store = px.bar(
            x=store_data.values,
            y=store_data.index,
            orientation='h',
            title='Revenue by Store',
            color=store_data.values,
            color_continuous_scale='Greens'
        )
        fig_store.update_layout(
            xaxis_title='Revenue ($)',
            yaxis_title='Store',
            showlegend=False,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_store, use_container_width=True)
    
    st.markdown("---")
    
    # =========================================================================
    # DISTRIBUTION ANALYSIS
    # =========================================================================
    
    st.header("📊 Distribution Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Channel Distribution
        channel_data = df_filtered.groupby('channel')['line_revenue'].sum()
        
        fig_channel = px.pie(
            values=channel_data.values,
            names=channel_data.index,
            title='Revenue by Channel',
            color_discrete_sequence=['#2ecc71', '#3498db']
        )
        fig_channel.update_traces(textposition='inside', textinfo='percent+label')
        fig_channel.update_layout(showlegend=False)
        st.plotly_chart(fig_channel, use_container_width=True)
    
    with col2:
        # Segment Distribution
        segment_data = df_filtered.groupby('customer_segment')['line_revenue'].sum()
        
        fig_segment = px.pie(
            values=segment_data.values,
            names=segment_data.index,
            title='Revenue by Segment',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_segment.update_traces(textposition='inside', textinfo='percent+label')
        fig_segment.update_layout(showlegend=False)
        st.plotly_chart(fig_segment, use_container_width=True)
    
    with col3:
        # Payment Distribution
        payment_data = df_filtered.groupby('payment_method')['line_revenue'].sum()
        
        fig_payment = px.pie(
            values=payment_data.values,
            names=payment_data.index,
            title='Revenue by Payment',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_payment.update_traces(textposition='inside', textinfo='percent+label')
        fig_payment.update_layout(showlegend=False)
        st.plotly_chart(fig_payment, use_container_width=True)
    
    st.markdown("---")
    
    # =========================================================================
    # TOP PERFORMERS
    # =========================================================================
    
    st.header("🏆 Top Performers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Products")
        top_products = df_filtered.groupby('product_name')['line_revenue'].sum().sort_values(ascending=False).head(10).reset_index()
        top_products.columns = ['Product', 'Revenue']
        top_products['Revenue'] = top_products['Revenue'].apply(lambda x: f"${x:,.2f}")
        top_products.index = range(1, len(top_products) + 1)
        st.dataframe(top_products, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Customers")
        top_customers = df_filtered.groupby('customer_id').agg({
            'line_revenue': 'sum',
            'customer_segment': 'first'
        }).sort_values('line_revenue', ascending=False).head(10).reset_index()
        top_customers.columns = ['Customer', 'Revenue', 'Segment']
        top_customers['Revenue'] = top_customers['Revenue'].apply(lambda x: f"${x:,.2f}")
        top_customers.index = range(1, len(top_customers) + 1)
        st.dataframe(top_customers, use_container_width=True)
    
    st.markdown("---")
    
    # =========================================================================
    # STORE PERFORMANCE TABLE
    # =========================================================================
    
    st.header("🏪 Store Performance Summary")
    
    store_summary = df_filtered.groupby('store_location').agg({
        'line_revenue': 'sum',
        'bill_id': 'nunique',
        'customer_id': 'nunique',
        'quantity': 'sum',
        'discount_applied': 'sum'
    }).reset_index()
    
    store_summary.columns = ['Store', 'Revenue', 'Bills', 'Customers', 'Units', 'Discounts']
    store_summary['Avg/Bill'] = store_summary['Revenue'] / store_summary['Bills']
    store_summary = store_summary.sort_values('Revenue', ascending=False)
    
    # Format for display
    display_summary = store_summary.copy()
    display_summary['Revenue'] = display_summary['Revenue'].apply(lambda x: f"${x:,.2f}")
    display_summary['Avg/Bill'] = display_summary['Avg/Bill'].apply(lambda x: f"${x:,.2f}")
    display_summary['Discounts'] = display_summary['Discounts'].apply(lambda x: f"${x:,.2f}")
    display_summary['Bills'] = display_summary['Bills'].apply(lambda x: f"{x:,}")
    display_summary['Customers'] = display_summary['Customers'].apply(lambda x: f"{x:,}")
    display_summary['Units'] = display_summary['Units'].apply(lambda x: f"{x:,}")
    
    st.dataframe(display_summary, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # =========================================================================
    # DATA PREVIEW & DOWNLOAD
    # =========================================================================
    
    st.header("📄 Data Preview & Export")
    
    with st.expander("View Filtered Data (First 50 rows)"):
        display_cols = ['transaction_id', 'date', 'store_location', 'customer_id',
                       'product_name', 'product_category', 'quantity', 'unit_price',
                       'discount_applied', 'line_revenue', 'channel', 'payment_method']
        st.dataframe(df_filtered[display_cols].head(50), use_container_width=True)
    
    # Download buttons
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_data,
            file_name="urbanmart_filtered_data.csv",
            mime="text/csv"
        )
    
    with col2:
        # Summary report
        summary = pd.DataFrame({
            'Metric': ['Total Revenue', 'Total Bills', 'Unique Customers', 'Units Sold', 'Total Discounts'],
            'Value': [f"${total_revenue:,.2f}", f"{total_bills:,}", f"{unique_customers:,}", 
                     f"{total_units:,}", f"${total_discount:,.2f}"]
        })
        summary_csv = summary.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Summary Report (CSV)",
            data=summary_csv,
            file_name="urbanmart_summary.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>🛒 UrbanMart Sales Dashboard | Q1-Q2 2025 Analysis</p>
            <p>Built with Python & Streamlit | © 2025 MAIB Student Project</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
