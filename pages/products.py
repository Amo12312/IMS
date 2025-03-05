import streamlit as st
import sqlite3
import speech_recognition as sr
import pyttsx3
import threading

st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(to bottom, #2c3e50, #3498db) !important;
            min-height: 100vh;
            overflow: auto;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #d6eaf8, #aed6f1) !important;
            color: black;
        }
        .stButton>button {
            border-radius: 10px;
            background-color: #3498db;
            color: white;
            font-size: 16px;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #2980b9;
        }
        .notification {
            background-color: #e74c3c;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect("inventory1.db")
    cursor = conn.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE COLLATE NOCASE,
            category TEXT,
            selling_price REAL,
            cost_price REAL,
            quantity INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def add_product(name, category, selling_price, cost_price):
    conn = sqlite3.connect("inventory1.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (name, category, selling_price, cost_price, quantity) VALUES (?, ?, ?, ?, 0)", 
                       (name, category, selling_price, cost_price))
        conn.commit()
        st.success(f"Product '{name}' added successfully!")
    except sqlite3.IntegrityError:
        st.error("Product already exists!")
    conn.close()


def update_quantity(name, new_quantity):
    conn = sqlite3.connect("inventory1.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products WHERE name = ?", (name,))
    if cursor.fetchone()[0] == 0:
        st.error(f"Product '{name}' not found! Cannot update quantity.")
        speak(f"Product {name} not found! Cannot update quantity.")
        conn.close()
        return

    cursor.execute("UPDATE products SET quantity = ? WHERE name = ?", (new_quantity, name))
    conn.commit()
    conn.close()
    st.success(f"Updated quantity of '{name}' to {new_quantity}!")
    speak(f"Updated quantity of {name} to {new_quantity}!")



def delete_product(name):
    conn = sqlite3.connect("inventory1.db")
    cursor = conn.cursor()

 
    cursor.execute("SELECT COUNT(*) FROM products WHERE name = ?", (name,))
    if cursor.fetchone()[0] == 0:
        st.error(f"Product '{name}' not found! Cannot delete.")
        speak(f"Product {name} not found! Cannot delete.")
        conn.close()
        return

    cursor.execute("DELETE FROM products WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    st.success(f"Product '{name}' has been deleted successfully!")
    speak(f"Product {name} has been deleted successfully!")



def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.UnknownValueError:
            st.warning("Could not understand audio.")
            return None
        except sr.RequestError:
            st.error("Speech recognition service is unavailable.")
            return None


def sell_product(name, sell_qty):
    conn = sqlite3.connect("inventory1.db")
    cursor = conn.cursor()

    cursor.execute("SELECT quantity FROM products WHERE name = ?", (name,))
    result = cursor.fetchone()

    if not result:
        st.error(f"Product '{name}' not found! Cannot sell.")
        speak(f"Product {name} not found! Cannot sell.")
        conn.close()
        return

    available_stock = result[0]

    if available_stock >= sell_qty:
        new_quantity = available_stock - sell_qty
        cursor.execute("UPDATE products SET quantity = ? WHERE name = ?", (new_quantity, name))
        conn.commit()
        conn.close()
        st.success(f"Sold {sell_qty} units of '{name}'. Updated stock: {new_quantity}")
        speak(f"Sold {sell_qty} units of {name}. Updated stock: {new_quantity}")
    else:
        st.warning(f"Not enough stock for '{name}'. Available stock: {available_stock}")
        speak(f"Not enough stock for {name}. Available stock: {available_stock}")


def handle_voice_commands():
    instruction_text = "Say: Add a product, Update quantity, Sell a product, Delete a product"
    st.info(instruction_text)
    speak(instruction_text)  
    
    command = recognize_speech()  
    if command:
        if "add" in command:
            st.info("Please say the product name to add.")
            speak("Please say the product name to add.")
            name = recognize_speech()
            
            if name:
                st.info(f"Product name: {name}")
                speak(f"Product name: {name}")
                
                st.info("Please say the category of the product.")
                speak("Please say the category of the product.")
                category = recognize_speech()
                
                if category:
                    st.info(f"Category: {category}")
                    speak(f"Category: {category}")
                    
                    st.info("Please say the cost price.")
                    speak("Please say the cost price.")
                    cost_price = recognize_speech()
                    
                    if cost_price:
                        try:
                            cost_price = float(cost_price)
                            st.info(f"Cost price: {cost_price}")
                            speak(f"Cost price: {cost_price}")
                            

                            st.info("Please say the selling price.")
                            speak("Please say the selling price.")
                            selling_price = recognize_speech()
                            

                            if selling_price:
                                try:
                                    selling_price = float(selling_price)
                                    st.info(f"Selling price: {selling_price}")
                                    speak(f"Selling price: {selling_price}")
                                    
                                    add_product(name, category, selling_price, cost_price)
                                except ValueError:
                                    st.warning("Could not recognize a valid selling price. Please try again.")
                                    speak("Could not recognize a valid selling price. Please try again.")
                        except ValueError:
                            st.warning("Could not recognize a valid cost price. Please try again.")
                            speak("Could not recognize a valid cost price. Please try again.")
        
        elif "update" in command:
            
            st.info("Please say the product name to update.")
            speak("Please say the product name to update.")
            name = recognize_speech()
            
            if name:
                st.info(f"Product name: {name}")
                speak(f"Product name: {name}")
                
               
                st.info("Please say the new quantity.")
                speak("Please say the new quantity.")
                
               
                new_quantity = None
                
                while new_quantity is None:
                    new_quantity = recognize_speech()
                    if new_quantity is None:
                        st.warning("Could not understand the quantity. Please try again.")
                        speak("Could not understand the quantity. Please try again.")
                    else:
                        try:
                            new_quantity = int(new_quantity)
                            st.info(f"New quantity: {new_quantity}")
                            speak(f"New quantity: {new_quantity}")
                            
                            
                            update_quantity(name, new_quantity)
                        except ValueError:
                            st.warning("Could not recognize a valid quantity. Please say it again.")
                            speak("Could not recognize a valid quantity. Please say it again.")
                            new_quantity = None
        
        elif "sell" in command:
            
            st.info("Please say the product name to sell.")
            speak("Please say the product name to sell.")
            name = recognize_speech()
            
            if name:
                st.info(f"Product name: {name}")
                speak(f"Product name: {name}")
                
               
                st.info("Please say the quantity sold.")
                speak("Please say the quantity sold.")
                
                sell_qty = None
                
                while sell_qty is None:
                    sell_qty = recognize_speech()
                    if sell_qty is None:
                        st.warning("Could not understand the quantity. Please try again.")
                        speak("Could not understand the quantity. Please try again.")
                    else:
                        try:
                            sell_qty = int(sell_qty)
                            st.info(f"Quantity sold: {sell_qty}")
                            speak(f"Quantity sold: {sell_qty}")
                            
                           
                            sell_product(name, sell_qty)
                        except ValueError:
                            st.warning("Could not recognize a valid quantity. Please say it again.")
                            speak("Could not recognize a valid quantity. Please say it again.")
                            sell_qty = None
        
        elif "delete" in command:
            
            st.info("Please say the product name to delete.")
            speak("Please say the product name to delete.")
            name = recognize_speech()
            
            if name:
                st.info(f"Product name: {name}")
                speak(f"Product name: {name}")
                
                delete_product(name)
        
        else:
            st.warning("Command not recognized. Try again!")

def products_page():
    st.title("🛒 MINI - MARKET Products 📦")
    init_db()

    mode = st.radio("Choose Mode:", ("Manual", "Voice"))

    if mode == "Manual":
        st.subheader("Manual Mode Enabled")
        
        st.subheader("Add new Product")
        name = st.text_input("Product Name")
        category = st.text_input("Category")
        selling_price = st.number_input("Selling Price", min_value=0.0, format="%.2f")
        cost_price = st.number_input("Cost Price", min_value=0.0, format="%.2f")
        
        if st.button("Add Product"):
            if name and category and selling_price > 0 and cost_price > 0:
                add_product(name, category, selling_price, cost_price)
            else:
                st.warning("Please fill in all fields correctly.")
        
        st.subheader("Update Product Quantity")
        product_name = st.selectbox("Select Product to Update", options=get_product_names())
        new_quantity = st.number_input("New Quantity", min_value=0, step=1)
        
        if st.button("Update Quantity"):
            if product_name and new_quantity >= 0:
                update_quantity(product_name, new_quantity)
            else:
                st.warning("Please provide valid inputs.")
        
        
        st.subheader("Delete Product")
        product_to_delete = st.selectbox("Select Product to Delete", options=get_product_names())
        
        if st.button("Delete Product"):
            if product_to_delete:
                delete_product(product_to_delete)
            else:
                st.warning("Please provide the product name to delete.")
        
       
        st.subheader("Sell Product")
        product_to_sell = st.selectbox("Select Product to Sell", options=get_product_names())
        sell_qty = st.number_input("Quantity to Sell", min_value=0, step=1)
        
        if st.button("Sell Product"):
            if product_to_sell and sell_qty > 0:
                sell_product(product_to_sell, sell_qty)
            else:
                st.warning("Please provide valid inputs.")
        
    else:
        st.subheader("Voice Mode Enabled")
        handle_voice_commands()


def get_product_names():
    conn = sqlite3.connect("inventory1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM products")
    products = cursor.fetchall()
    conn.close()
    return [product[0] for product in products]


if __name__ == "__main__":
    products_page()