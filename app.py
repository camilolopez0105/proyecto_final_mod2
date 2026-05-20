
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Brazilian E-commerce Analysis", layout="wide")

# Custom CSS for Brazilian theme
st.markdown("""
    <style>
    .stApp {
        background-color: #8fa885;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📊 Brazilian E-commerce Analysis Dashboard")
st.markdown("Here we analyze the Brazilian E-commerce dataset, we will see relevant and important information such as total number of orders, total sales and best of all, with the option to filter everything by State!")

df = pd.read_pickle('dataset_analitico.pkl')

# Sidebar
st.sidebar.header("Filters")
selected_state = st.sidebar.selectbox("Select State", ['All'] + list(df['customer_state'].unique()))

# Filter data based on selection
if selected_state == 'All':
    filtered_df = df
else:
    filtered_df = df[df['customer_state'] == selected_state]

# Metric cards
total_orders = filtered_df.shape[0]
total_sales = filtered_df['price'].sum()
total_customers = filtered_df['customer_city'].nunique()
avg_order_value = total_orders / total_orders if total_orders > 0 else 0
avg_freight = filtered_df['freight_value'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Selected State", selected_state)
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Total Customers", f"{total_customers:,}")
col4.metric("Average Freight", f"R$ {avg_freight:,.2f}")

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"R$ {total_sales:,.2f}")
col2.metric("Total Revenue", f"R$ {total_sales + filtered_df['freight_value'].sum():,.2f}")
col3.metric("Average Order Value", f"R$ {total_sales/total_orders:,.2f}" if total_orders > 0 else "R$ 0.00")

# Main content
st.header(f"Analysis for {selected_state if selected_state != 'All' else 'All States'}")

# Top 20 cities by orders
cities_data = filtered_df.groupby(['customer_state', 'customer_city']).agg(
    order_count=('order_id', 'count'),
    total_sales=('price', 'sum')
).reset_index()

col1, col2 = st.columns(2)

with col1:
    cities_by_sales = cities_data.sort_values('total_sales', ascending=True).tail(20)
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    bars1 = ax1.barh(cities_by_sales['customer_city'], cities_by_sales['total_sales'], color='#009c3b')
    ax1.set_title(f'Top 20 Cities by Total Sales', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Total Sales (R$)', fontsize=12)
    ax1.set_ylabel('City', fontsize=12)
    ax1.grid(True, alpha=0.3, axis='x')
    for i, sales in enumerate(cities_by_sales['total_sales']):
        ax1.text(sales + sales*0.01, i, f'R$ {sales:,.0f}', va='center', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig1)

with col2:
    cities_by_orders = cities_data.sort_values('order_count', ascending=True).tail(20)
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    bars2 = ax2.barh(cities_by_orders['customer_city'], cities_by_orders['order_count'], color='#002776')
    ax2.set_title(f'Top 20 Cities by Number of Orders', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Number of Orders', fontsize=12)
    ax2.set_ylabel('City', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='x')
    for i, count in enumerate(cities_by_orders['order_count']):
        ax2.text(count + count*0.01, i, str(count), va='center', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig2)

# Display table
st.subheader("Top 20 Cities Data")
st.dataframe(cities_data.sort_values('total_sales', ascending=False).head(20))

# Additional charts
if selected_state == 'All':
    st.subheader("Total Sales by State")
    state_sales = df.groupby('customer_state')['price'].sum().sort_values(ascending=False)
    st.bar_chart(state_sales)
    
    st.subheader("Number of Orders by State")
    state_orders = df.groupby('customer_state').size().sort_values(ascending=False)
    st.bar_chart(state_orders)
else:
    st.subheader(f"Orders and Sales by City in {selected_state}")
    city_data = filtered_df.groupby('customer_city').agg(
        orders=('order_id', 'count'),
        sales=('price', 'sum')
    ).sort_values('sales', ascending=False)
    st.bar_chart(city_data['sales'])
    st.bar_chart(city_data['orders'])

# Temporal analysis
st.subheader("Temporal Analysis")

if 'order_date' in filtered_df.columns:
    filtered_df = filtered_df.copy()
    filtered_df['order_month'] = pd.to_datetime(filtered_df['order_date'], errors='coerce').dt.to_period('M')
    filtered_df['order_year'] = pd.to_datetime(filtered_df['order_date'], errors='coerce').dt.year
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_data = filtered_df.groupby('order_month').size()
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.bar(range(len(monthly_data)), monthly_data.values, color='#ffdf00')
        ax1.set_title('Orders by Month', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Month', fontsize=12)
        ax1.set_xticks(range(len(monthly_data)))
        ax1.set_xticklabels([str(m) for m in monthly_data.index], rotation=45, ha='right')
        ax1.get_yaxis().set_visible(False)
        for i, v in enumerate(monthly_data.values):
            ax1.text(i, v + v*0.01, f'{v:,}', ha='center', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig1)
    
    with col2:
        yearly_data = filtered_df.groupby('order_year').size()
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.bar(yearly_data.index.astype(str), yearly_data.values, color='#009c3b')
        ax2.set_title('Orders by Year', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Year', fontsize=12)
        ax2.get_yaxis().set_visible(False)
        for i, v in enumerate(yearly_data.values):
            ax2.text(i, v + v*0.02, f'{v:,}', ha='center', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig2)

# Analytical Conclusion
st.subheader("📝 Analytical Conclusion")

st.markdown("""
**Key Findings:**

- **Market Concentration:** São Paulo (SP) dominates the Brazilian e-commerce market, accounting for **42%** of total sales (R$ 4.6M) and **42%** of all orders (40,501). Rio de Janeiro (RJ) and Minas Gerais (MG) follow as secondary markets.

- **Top Performing City:** São Paulo city alone generates **R$ 1.68M** in sales, representing nearly 14% of total revenue - making it the single most important e-commerce hub in Brazil.

- **Sales vs. Orders Correlation:** Cities with higher sales generally align with those having more orders, indicating consistent buying patterns across the country.

- **Growth Trend:** 2017 and 2018 show significant activity, with the dataset spanning 2016-2018, showing steady e-commerce adoption in Brazil.

- **Shipping Costs:** Average freight adds approximately **10%** to the total order value, a key factor for pricing strategies.
""")
