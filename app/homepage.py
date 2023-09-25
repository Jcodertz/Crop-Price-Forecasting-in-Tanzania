import streamlit as st
import random

# Define a list of random crop facts(Did You Know?)
crop_facts = [
    "Maize is one of the oldest cultivated crops, dating back thousands of years.",
    "Beans are an excellent source of fiber, vitamins, and minerals.",
    "Rice is the primary food source for over half of the world's population.",
    "Tanzania is one of the top maize-producing countries in Africa.",
    "Beans are often called the 'poor man's meat' due to their high protein content.",
    "Beans, rice, and maize are vital staples in Tanzanian cuisine.",
    "Beans are a good source of protein, a dietary essential in Tanzania.",
    "Rice is commonly enjoyed as one of the main dish in Tanzanian meals.",
    "Beans are often used in Tanzanian stews and soups.",
    "Maize is used to make ugali, a popular Tanzanian dish.",
    "Beans are commonly used in Tanzanian street food.",
    "Rice is a key ingredient in Tanzanian biryani dishes.",
    "Rice is a primary crop in the Morogoro region of Tanzania.",
    "Rice paddies provide habitat for diverse bird species in Tanzania.",
]

# Define a function for the home page
def home_page():
    # Header
    st.markdown("<h1 style='text-align: center;'>Introducing Our App: Crop Price Forecasting in Tanzania</h1>", unsafe_allow_html=True)

    # Project Focus: Price Forecasting of Maize, Rice, and Beans
    st.markdown("## Project Focus: Price Forecasting of Maize, Rice, and Beans in Tanzania")

    st.write("Our project is dedicated to forecasting the prices of three crucial crops in Tanzania: maize, rice, and beans. These staple crops are essential for food security and livelihoods in the region. Through advanced data analysis and predictive models, we aim to provide farmers and stakeholders with accurate price forecasts for these key commodities.")

    # Crop images in three columns
    col11, col21, col31 = st.columns(3)

    # Define crop images
    crop_images = {
        "Maize": "./images/maize.jpg",
        "Beans": "./images/beans.jpg",
        "Rice": "./images/Rice.jpg"
    }

    # Display crop images in columns
    with col11:
        st.image(crop_images["Maize"], width=200,  caption="Maize")
    with col21:
        st.image(crop_images["Beans"], width=200, caption="Beans")
    with col31:
        st.image(crop_images["Rice"], width=200, caption="Rice")

    crop_data = {
        "Maize": {
            "icon": "🌽",
            "help": "Click to Learn More About Maize",
            "info": "Maize is a staple crop in Tanzania with a current price of 1,014 TZS per kg.",
            "conditions": "Maize thrives in well-drained soil and requires moderate rainfall and sunlight.",
            "common_growing_regions": "Common regions for maize cultivation in Tanzania include Arusha and Kilimanjaro.",
            "uses": "Maize is used for various purposes, including human consumption, animal feed, and industrial processing."
        },
        "Beans": {
            "icon": "🌱",
            "help": "Click to Learn More About Beans",
            "info": "Beans are a nutritious crop with a current price of 2,567 TZS per kg.",
            "conditions": "Beans grow well in regions with consistent rainfall and moderate temperatures.",
            "common_growing_regions": "Common regions for beans cultivation in Tanzania include Mbeya and Iringa.",
            "uses": "Beans are a good source of protein and are consumed in various dishes in Tanzanian cuisine."
        },
        "Rice": {
            "icon": "🍚",
            "help": "Click to Learn More About Rice",
            "info": "Rice is a widely consumed crop with a current price of 2,415 TZS per kg.",
            "conditions": "Rice requires flooded fields for cultivation and is grown in regions like Morogoro and Shinyanga.",
            "common_growing_regions": "Common regions for rice cultivation in Tanzania include Morogoro and Shinyanga.",
            "uses": "Rice is a staple food in Tanzania and is consumed in various forms, including steamed rice and rice-based dishes."
        }
    }

    for crop_name, crop_info in crop_data.items():
        with col11 if crop_name == "Maize" else col21 if crop_name == "Beans" else col31:
            if st.button(f"{crop_info['icon']} {crop_name}", help=crop_info["help"]):
                st.write(crop_info["info"])
                st.markdown(f"**Favorable Conditions in Tanzania:** {crop_info['conditions']}")
                st.markdown(f"**Common Growing Regions:** {crop_info['common_growing_regions']}")
                st.markdown(f"**Uses:** {crop_info['uses']}")

    st.markdown("## Unlocking the Power of Data for Tanzanian Farmers")

    # Introduction
    st.write("In the heart of East Africa, where agriculture plays a vital role in both the economy and the daily lives of millions, we bring you a powerful tool designed to empower Tanzanian farmers and stakeholders in the agriculture industry. Our Streamlit app, dedicated to crop price forecasting in Tanzania, is a game-changer for those looking to make informed decisions in this dynamic field.")

    # The Agricultural Landscape in Tanzania
    st.markdown("## The Agricultural Landscape in Tanzania")
    st.write("Tanzania is known for its diverse agricultural sector, with a range of crops cultivated across the country. From maize and rice to coffee and cashew nuts, the agriculture industry is a significant contributor to the nation's GDP. However, the prices of these crops can be highly variable, influenced by numerous factors such as weather patterns, market demand, and global trends.")

    # Bridging the Information Gap
    st.markdown("## Bridging the Information Gap")
    st.write("One of the challenges faced by Tanzanian farmers and stakeholders is the lack of access to timely and accurate crop price information. Without this critical data, making informed decisions about planting, harvesting, and selling crops becomes challenging. That's where our Streamlit app steps in.")
    

    # Empowering Tanzanian Agriculture
    st.markdown("## Empowering Tanzanian Agriculture")
    st.write("Our mission is to empower Tanzanian farmers, traders, and policymakers with the data they need to thrive in the ever-changing world of agriculture. By providing accurate crop price forecasts and historical trends, we aim to level the playing field and contribute to the growth of this vital sector.")

    st.write("*Note: The information provided by our app is for informational purposes only and should not replace professional advice. Always consult with experts and local authorities when making significant agricultural decisions.*")

    # Random Crop Fact section
    st.markdown('<div align="center">', unsafe_allow_html=True)
    st.markdown("## Did You Know?")
    if st.button("Generate"):
        random_fact = random.choice(crop_facts)
        st.info(f"Crop Fact: {random_fact}")


    st.markdown('***')

    # Create two columns for dLab information and development team credits
    col1, col2 = st.columns(2)

    # dLab Tanzania information
    with col1:
        st.image('./images/dLab_logo.png', width=100)
        st.write("dLab Tanzania")
        st.write("Address Line: P. O. Box 33335, DSM")
        st.write("Email Address: connect@dlab.or.tz")
        st.write("Phone Number: 0225 222 410 645 / 0222 410 690")

    # Development team credits
    with col2:
        st.markdown("### Development Team")
        st.write("Meet the talented individuals who made this app possible:")
        st.write("- Juma Omar, Email: jumaomar97@gmail.com")
        st.write("- Basilisa Katani, Email: lisakatani1008@gmail.com")
        st.write("- James Loma, Email: jamesloma80@gmail.com")
        st.write("- Geoffrey Muchunguzi, Email: geoffreymuchunguzi@gmail.com")
        st.write("We appreciate their dedication and creativity in making this app extraordinary!")
