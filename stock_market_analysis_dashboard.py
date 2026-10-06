import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# --- Page Configuration ---
st.set_page_config(
    page_title="Stock Market Analytics Dashboard",
    layout="wide"
)

# --- Title and Header ---
st.title("Stock Market Analysis And Signal Dashboard")
st.markdown("Automated technical trend analysis, buy/sell signal detection, and return comparison.")

# --- Step A: Data Loading (MySQL with CSV Fallback) ---
@st.cache_data
def load_data():
    try:
        # Replace with your MySQL credentials
        engine = create_engine("mysql+mysqlconnector://root:password@localhost/stock_db")
        query = "SELECT Stock_Name, Date, Closing_Price FROM stock_prices ORDER BY Stock_Name, Date"
        data = pd.read_sql(query, engine)
        st.sidebar.success(" Connected to MySQL database")
    except Exception as e:
        # Fallback to local CSV if MySQL is unreachable
        data = pd.read_csv(r'C:\aFiles And Media\DataAnalytics\HexaSolutions\Hexa Assignments\Assignments To Submit 09-10-2026\SQL Stock Marketing Assignment\7- SQL Stock Marketing Assignment\SQL - Stock Market Analysis Project\master_stock_prices.csv')
        st.sidebar.info(" Loaded from local CSV file (MySQL offline)")
    
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by=['Stock_Name', 'Date'], inplace=True)
    return data

df = load_data()

# --- Step B: Sidebar Controls ---
st.sidebar.header("Filter Options")
stock_list = sorted(df['Stock_Name'].unique().tolist())
selected_stock = st.sidebar.selectbox("Select a Company", stock_list, index=0)

min_date = df['Date'].min().date()
max_date = df['Date'].max().date()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter by selected date range
if len(date_range) == 2:
    start_filter, end_filter = date_range
    filtered_df = df[(df['Date'].dt.date >= start_filter) & (df['Date'].dt.date <= end_filter)]
else:
    filtered_df = df.copy()

# Focus dataframe for the selected stock
stock_df = filtered_df[filtered_df['Stock_Name'] == selected_stock].copy()

# --- Step C: Compute Metrics and Buy/Sell Signals ---
if not stock_df.empty:
    # 1. Running Average and Signals
    stock_df['Running_Avg'] = stock_df['Closing_Price'].expanding().mean()
    stock_df['Signal'] = stock_df.apply(
        lambda r: 'BUY' if r['Closing_Price'] > r['Running_Avg'] else 'SELL', axis=1
    )

    start_price = stock_df.iloc[0]['Closing_Price']
    end_price = stock_df.iloc[-1]['Closing_Price']
    min_price = stock_df['Closing_Price'].min()
    max_price = stock_df['Closing_Price'].max()
    overall_change = ((end_price - start_price) / start_price) * 100
    potential_profit = ((max_price - min_price) / min_price) * 100

    # --- Step D: Display Top Metric Cards ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current / Latest Price", f"₹{end_price:,.2f}", f"{overall_change:.2f}%")
    col2.metric("Min Closing Price", f"₹{min_price:,.2f}")
    col3.metric("Max Closing Price", f"₹{max_price:,.2f}")
    col4.metric("Max Profit Potential", f"{potential_profit:.2f}%")

    st.markdown("---")

    # --- Step E: Interactive Stock Chart with Buy/Sell Signals ---
    st.subheader(f"Price Trend & Dynamic Buy/Sell Signals: {selected_stock}")
    
    fig = go.Figure()

    # Price Line
    fig.add_trace(go.Scatter(
        x=stock_df['Date'], 
        y=stock_df['Closing_Price'], 
        mode='lines', 
        name='Closing Price',
        line=dict(color='blue', width=2)
    ))

    # Historical Running Average Line
    fig.add_trace(go.Scatter(
        x=stock_df['Date'], 
        y=stock_df['Running_Avg'], 
        mode='lines', 
        name='Running Avg Baseline',
        line=dict(color='yellow', width=1.5, dash='dash')
    ))

    # Buy Signals (Green points)
    buys = stock_df[stock_df['Signal'] == 'BUY']
    fig.add_trace(go.Scatter(
        x=buys['Date'], 
        y=buys['Closing_Price'], 
        mode='markers', 
        name='Buy Signal (Above Avg)',
        marker=dict(symbol='triangle-up', size=5, color='#10B981')
    ))

    # Sell Signals (Red points)
    sells = stock_df[stock_df['Signal'] == 'SELL']
    fig.add_trace(go.Scatter(
        x=sells['Date'], 
        y=sells['Closing_Price'], 
        mode='markers', 
        name='Sell Signal (Below Avg)',
        marker=dict(symbol='triangle-down', size=5, color='#EF4444')
    ))

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Step F: Comparative Analysis (All Stocks) ---
st.markdown("---")
st.subheader("Comparative Market Performance (Start vs. End Date)")

# Calculate overall percentage returns across all stocks in selected window
summary_data = []
for name, group in filtered_df.groupby('Stock_Name'):
    g_sorted = group.sort_values('Date')
    if not g_sorted.empty:
        s_p = g_sorted.iloc[0]['Closing_Price']
        e_p = g_sorted.iloc[-1]['Closing_Price']
        pct = ((e_p - s_p) / s_p) * 100
        summary_data.append({'Stock Name': name, 'Start Price (₹)': s_p, 'End Price (₹)': e_p, 'Percentage Change (%)': round(pct, 2)})

summary_df = pd.DataFrame(summary_data).sort_values(by='Percentage Change (%)', ascending=False)

comp_col1, comp_col2 = st.columns([1, 1])

with comp_col1:
    bar_fig = px.bar(
        summary_df,
        x='Stock Name',
        y='Percentage Change (%)',
        color='Percentage Change (%)',
        color_continuous_scale='Tealgrn',
        text='Percentage Change (%)',
        title="Overall Return Ranking (%)"
    )
    bar_fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    bar_fig.update_layout(template="plotly_white")
    st.plotly_chart(bar_fig, use_container_width=True)

with comp_col2:
    st.markdown("### Performance Summary Table")
    st.dataframe(summary_df.reset_index(drop=True), use_container_width=True)