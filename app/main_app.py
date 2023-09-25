import streamlit as st
from homepage import home_page
from dashboard import dashboard_page
from forecasting import forecasting_page

# Create a Streamlit app
def main():
    st.set_page_config(page_title="Crop Price Forecasting in Tanzania", layout='wide', page_icon='🌾')

    # Display an image from a local file
    image_path = "../images/crop2.png"
    st.image(image_path, use_column_width=True)
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ("🏠Home", "📈Dashboard", "📅Forecasting"))

    st.sidebar.markdown("---")

    st.sidebar.image('../images/crop.jpg', use_column_width=True, caption='Empowering Agriculture with Data')

    st.sidebar.markdown("---")

    st.sidebar.text("ⓒ 2023 dLab Tanzania")

    if page == '🏠Home':
        home_page()
    elif page == "📈Dashboard":
        dashboard_page()
    elif page == "📅Forecasting":
        forecasting_page()

if __name__ == "__main__":
    main()

