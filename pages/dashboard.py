import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown("""
    <style>
    /* Full-screen background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom, #2c3e50, #3498db) !important;
        min-height: 100vh; 
        overflow: auto;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #d6eaf8, #aed6f1) !important;
        color: black !important;
    }

    /* Centering titles and subtitles */
    .center-text {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

def get_product_data():
    conn = sqlite3.connect("inventory1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, quantity, cost_price, selling_price FROM products")
    products = cursor.fetchall()
    conn.close()
    return products


def create_dashboard():
    st.markdown("<h1 class='center-text'>🛒 MINI - MARKET Dashboard</h1>", unsafe_allow_html=True)
    
   
    products = get_product_data()
    
    
    product_names = []
    profits = []
    quantities = []
    for product in products:
        name, quantity, cost_price, selling_price = product
        profit = (selling_price - cost_price) * quantity  # Calculate profit for each product
        product_names.append(name)
        profits.append(profit)
        quantities.append(quantity)
    
    
    profit_data = pd.DataFrame({'Product Name': product_names, 'Profit': profits})
    profit_data = profit_data.sort_values(by='Profit', ascending=False)
    
    
    seasonality_data = pd.DataFrame({'Product Name': product_names, 'Available Quantity': quantities})
    seasonality_data = seasonality_data.sort_values(by='Available Quantity', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Profit per Product")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x='Profit', y='Product Name', data=profit_data, ax=ax, palette="viridis")
        ax.set_title("Profit per Product")
        ax.set_xlabel("Profit (in ₹)")
        ax.set_ylabel("Product Name")
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Profit Share Product")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.pie(profit_data['Profit'], labels=profit_data['Product Name'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3", len(profit_data)))
        ax2.axis('equal')  
        st.pyplot(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🗓️ Product Stock Seasonality")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.barplot(x='Available Quantity', y='Product Name', data=seasonality_data, ax=ax3, palette="coolwarm")
        ax3.set_title("Stock Seasonality")
        ax3.set_xlabel("Available Quantity")
        ax3.set_ylabel("Product Name")
        st.pyplot(fig3, use_container_width=True)
    
    with col4:
        st.subheader("📊 Distribution of Available Quantity")
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        ax4.hist(seasonality_data['Available Quantity'], bins=10, color='skyblue', edgecolor='black')
        ax4.set_title("Distribution of Product Stock")
        ax4.set_xlabel("Available Quantity")
        ax4.set_ylabel("Frequency")
        st.pyplot(fig4, use_container_width=True)
    
    # Scatter Plot: Profit vs Available Quantity
    st.subheader("🔴 Profit vs Available Quantity")
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    ax5.scatter(seasonality_data['Available Quantity'], profit_data['Profit'], color='orange')
    ax5.set_title("Profit vs Available Quantity")
    ax5.set_xlabel("Available Quantity")
    ax5.set_ylabel("Profit (in ₹)")
    st.pyplot(fig5, use_container_width=True)
    
if __name__ == "__main__":
    create_dashboard()
