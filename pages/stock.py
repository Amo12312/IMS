import pandas as pd
import streamlit as st
import sqlite3

st.markdown("""
    <style>
    /* Full-screen background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom, #2c3e50, #3498db) !important;
        min-height: 100vh; 
        overflow: auto;
    }

    # /* Ensure scrolling works */
    # html, body, [class*="st-emotion-cache"] {
    #     height: auto !important;
    #     overflow: auto !important;
    # }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #d6eaf8, #aed6f1) !important;
        color: black !important;
    }

    /* Sidebar text color */
    [data-testid="stSidebarContent"] * {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

def stock_page():
    st.title("🛒 MINI - MARKET STOCKS")
    
    conn = sqlite3.connect("inventory1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, quantity, cost_price, selling_price FROM products")
    products = cursor.fetchall()
    conn.close()

    if products:
        low_stock_products = [product for product in products if product[2] < 5]  

        if low_stock_products:
            for product in low_stock_products:
                st.markdown(
                    f"""
                    <style>
                    .notification {{
                        position: fixed;
                        top: 120px;
                        right: 20px;
                        background-color: #f44336;
                        color: white;
                        padding: 10px;
                        border-radius: 5px;
                        font-weight: bold;
                        z-index: 9999;
                    }}
                    </style>
                    <div class="notification">
                        Low stock for {product[1]}! Only {product[2]} left.
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        
        st.subheader("🔍 Search & Filter Stock")

        search_query = st.text_input("Search by Product Name").strip()
        
        stock_level = st.selectbox("Filter by Stock Level", ["All", "Low Stock", "Out of Stock", "In Stock"])

        sort_order = st.selectbox("Sort Alphabetically", ["None", "A-Z", "Z-A"])

        if search_query:
            products = [product for product in products if search_query.lower() in product[1].lower()]

        if stock_level == "Low Stock":
            products = [product for product in products if product[2] < 5]  # threshold of 5 for low stock
        elif stock_level == "Out of Stock":
            products = [product for product in products if product[2] == 0]
        elif stock_level == "In Stock":
            products = [product for product in products if product[2] > 0]

 
        if sort_order == "A-Z":
            products.sort(key=lambda x: x[1].lower())  
        elif sort_order == "Z-A":
            products.sort(key=lambda x: x[1].lower(), reverse=True)  

        data = []
        for idx, product in enumerate(products, 1):
            product_id, name, quantity, cost_price, selling_price = product
            data.append([idx, name, quantity, cost_price, selling_price])

        df = pd.DataFrame(data, columns=["Sr. No.", "Product Name", "Available Quantity", "Buying Price", "Selling Price"])
        st.dataframe(df)
    else:
        st.warning("No products available in the inventory.")

if __name__ == "__main__":
    stock_page()


