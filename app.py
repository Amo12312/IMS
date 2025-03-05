import streamlit as st

st.markdown("""
    <style>
    /* Use elegant fonts */
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap');
    
    /* Full-screen background with elegant gradient */
    body {
        margin: 0;
        padding: 0;
        background: linear-gradient(to bottom, #2c3e50, #3498db);
        background-size: cover;
        background-position: center;
        font-family: 'Lora', serif;
        height: 100vh;
    }
    
    /* Remove Streamlit padding and ensure full coverage */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom, #2c3e50, #3498db) !important;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #f7f7f7, #e5e5e5) !important;
        color: #333 !important;
    }
    
    /* Centered content */
    .main-content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        text-align: center;
        padding: 0 20px;
        max-width: 600px;
    }

    /* Header Styling */
    .header {
        font-size: 4.8em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #fff;
        text-shadow: 4px 4px 12px rgba(0, 0, 0, 0.3);
        margin-bottom: 10px;
    }
    
    /* Subheader styling */
    .subheader {
        font-size: 2.2em;
        font-weight: 500;
        color: #f39c12;
        text-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3);
        margin-bottom: 40px;
    }

    /* Action button design with transition */
    .action-button {
        background-color: #f39c12;
        color: white;
        padding: 18px 50px;
        font-size: 1.4em;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    }
    .action-button:hover {
        background-color: #e67e22;
        transform: scale(1.1);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.4);
    }
    </style>
""", unsafe_allow_html=True)


def front_page():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    st.markdown("<h1 class='header'>Welcome to 🛒 Mini - Market</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Your One-Stop Shop for Freshness and Quality! 😎</p>", unsafe_allow_html=True)

    if st.button('Start Shopping', key='shopping', help="Browse products and make purchases!"):
        st.write("Shopping feature coming soon!")

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    front_page()
