import xgboost as xgb
import time
import pandas as pd
import streamlit as st
import joblib

# Define a function for the model prediction page
def forecasting_page():
    
    # Load your saved model
    xgb_model = joblib.load('./model/xgb_model.pkl')

    # Load the mappings for conversion
    regional_mapping = {
        'Arusha': 0,
        'Dar-es-salaam': 1,
        'Dodoma': 2,
        'Iringa': 3,
        'Kagera': 4,
        'Kigoma': 5,
        'Kilimanjaro': 6,
        'Lindi': 7,
        'Manyara': 8,
        'Mara': 9,
        'Mbeya': 10,
        'Morogoro': 11,
        'Mtwara': 12,
        'Mwanza': 13,
        'Rukwa': 14,
        'Ruvuma': 15,
        'Shinyanga': 16,
        'Singida': 17,
        'Tabora': 18,
        'Tanga': 19,
        'Katavi': 20,
        'Njombe': 21,
        'Geita': 22
    }
    
    district_mapping = {
        'Arusha Urban': 0,
        'Ilala': 1,
        'Mpwapwa': 2,
        'Iringa Urban': 3,
        'Bukoba Urban': 4,
        'Kigoma Municipal-Ujiji': 5,
        'Moshi Municipal': 6,
        'Lindi Urban': 7,
        'Babati Urban': 8,
        'Musoma Municipal': 9,
        'Mbeya Urban': 10,
        'Morogoro Urban': 11,
        'Mtwara Urban': 12,
        'Nyamagana': 13,
        'Sumbawanga Urban': 14,
        'Songea Urban': 15,
        'Shinyanga Urban': 16,
        'Singida Urban': 17,
        'Tabora Urban': 18,
        'Tanga': 19,
        'Mpanda Urban': 20,
        "Wanging'ombe": 21,
        'Geita': 22,
        'Kinondoni': 23,
        'Temeke': 24,
        'Kongwa': 25
    }  
    
    market_mapping = {
        'Arusha (urban)': 0,
        'Dar Es Salaam': 1,
        'Dodoma (Majengo)': 2,
        'Iringa Urban': 3,
        'Bukoba': 4,
        'Kigoma': 5,
        'Moshi': 6,
        'Lindi': 7,
        'Babati': 8,
        'Musoma': 9,
        'Mwanjelwa': 10,
        'Morogoro': 11,
        'Mtwara DC': 12,
        'Mwanza': 13,
        'Sumbawanga': 14,
        'Songea': 15,
        'Shinyanga': 16,
        'Singida': 17,
        'Tabora': 18,
        'Tanga / Mgandini': 19,
        'Mpanda': 20,
        'Njombe': 21,
        'Geita': 22,
        'Ilala (Buguruni)': 23,
        'Kinondoni (Tandale)': 24,
        'Temeke (Tandika)': 25,
        'Kibaigwa': 26,
        'Mbeya (SIDO)': 27,
        'Tanga': 28,
        'Sumbawanga (Katumba)': 29
    }
    
    commodity_mapping = {
        'Maize': 0,
        'Rice': 1,
        'Beans': 2,
    }

    st.markdown("## Welcome! Select your options and we'll predict the crop price for you!")

    # Collect user inputs
    st.subheader('Input Details')

    # Select regional
    selected_regional = st.selectbox('Select Regional', sorted(regional_mapping.keys()))

    # Define a dictionary to map regions to their respective districts and markets
    region_to_districts = {
        'Arusha': ['Arusha Urban'],
        'Dar-es-salaam': ['Ilala', 'Kinondoni', 'Temeke'],
        'Dodoma': ['Mpwapwa', 'Kongwa'],
        'Iringa': ['Iringa Urban'],
        'Kagera': ['Bukoba Urban'],
        'Kigoma': ['Kigoma Municipal-Ujiji'],
        'Kilimanjaro': ['Moshi Municipal'],
        'Lindi': ['Lindi Urban'],
        'Manyara': ['Babati Urban'],
        'Mara': ['Musoma Municipal'],
        'Mbeya': ['Mbeya Urban'],
        'Morogoro': ['Morogoro Urban'],
        'Mtwara': ['Mtwara Urban'],
        'Mwanza': ['Nyamagana'],
        'Rukwa': ['Sumbawanga Urban'],
        'Ruvuma': ['Songea Urban'],
        'Shinyanga': ['Shinyanga Urban'],
        'Singida': ['Singida Urban'],
        'Tabora': ['Tabora Urban'],
        'Tanga': ['Tanga'],
        'Katavi': ['Mpanda Urban'],
        'Njombe': ["Wanging'ombe"],
        'Geita': ['Geita'],
    }
    
    region_to_markets = {
        'Arusha': ['Arusha (urban)'],
        'Dar-es-salaam': ['Dar Es Salaam', 'Ilala (Buguruni)', 'Kinondoni (Tandale)', 'Temeke (Tandika)'],
        'Dodoma': ['Dodoma (Majengo)', 'Kibaigwa'],
        'Iringa': ['Iringa Urban'],
        'Kagera': ['Bukoba'],
        'Kigoma': ['Kigoma'],
        'Kilimanjaro': ['Moshi'],
        'Lindi': ['Lindi'],
        'Manyara': ['Babati'],
        'Mara': ['Musoma'],
        'Mbeya': ['Mwanjelwa', 'Mbeya (SIDO)'],
        'Morogoro': ['Morogoro'],
        'Mtwara': ['Mtwara DC'],
        'Mwanza': ['Mwanza'],
        'Rukwa': ['Sumbawanga', 'Sumbawanga (Katumba)'],
        'Ruvuma': ['Songea'],
        'Shinyanga': ['Shinyanga'],
        'Singida': ['Singida'],
        'Tabora': ['Tabora'],
        'Tanga': ['Tanga / Mgandini', 'Tanga'],
        'Katavi': ['Mpanda'],
        'Njombe': ['Njombe'],
        'Geita': ['Geita'],
    }
    
    # Get the districts and markets based on the selected regional
    selected_district = st.selectbox('Select District', region_to_districts[selected_regional])
    selected_market = st.selectbox('Select Market', region_to_markets[selected_regional])

    commodity = st.selectbox('Select Commodity', sorted(commodity_mapping.keys()))
    year = st.number_input('Enter Year', min_value=2023, max_value=2023, value=2023)
    month = st.number_input('Enter Month', min_value=6, max_value=12, value=6)

    # Improve button style
    predict_button = st.button('Predict', key='predict_button', help='Click to make a prediction')

    # Use colorful headers
    st.subheader('Prediction Result')

    # Custom text style
    st.markdown("**Disclaimer**: The prediction is for informational purposes only and may not reflect real-world prices accurately.")

    # Define the predict_crop_price function
    def predict_crop_price(regional, district, market, commodity, year, month):
        # Convert user inputs to the numerical format (replace with your mappings)
        regional = regional_mapping[regional]
        district = district_mapping[district]
        market = market_mapping[market]
        commodity = commodity_mapping[commodity]

        # Create a DataFrame with the user inputs
        input_data = pd.DataFrame({
            'regional': [regional],
            'district': [district],
            'market': [market],
            'commodity': [commodity],
            'year': [year],
            'month': [month]
        })

        # Simulate prediction delay (replace with actual prediction)
        time.sleep(2)

        # Make a prediction
        prediction = xgb_model.predict(input_data)[0]

        # Format the prediction with thousand separators
        formatted_prediction = '{:,.2f} TZS'.format(prediction)

        return formatted_prediction

    # Progress indicator
    if predict_button:
        with st.spinner('Predicting...'):
            formatted_prediction = predict_crop_price(selected_regional, selected_district, selected_market, commodity, year, month)
            st.success('Prediction complete')
            st.write(f'Predicted Price: {formatted_prediction}')
            st.write("NOTE: Prediction is for 100kg, typically considered as a wholesale quantity.")
            st.write("Prices for 1kg may vary and are often different, especially in retail markets.")
   
    st.markdown("---")

    # Create two columns for dLab information and development team credits
    co1, co2 = st.columns(2)

    # dLab Tanzania information
    with co1:
        st.image('./images/dlab_logo.png', width=100)
        st.write("dLab Tanzania")
        st.write("Address Line: P. O. Box 33335, DSM")
        st.write("Email Address: connect@dlab.or.tz")
        st.write("Phone Number: 0225 222 410 645 / 0222 410 690")

    # Development team credits
    with co2:
        st.markdown("### Development Team")
        st.write("Meet the talented individuals who made this app possible:")
        st.write("- Juma Omar, Email: jumaomar97@gmail.com")
        st.write("- Basilisa Katani, Email: lisakatani1008@gmail.com")
        st.write("- James Loma, Email: jamesloma80@gmail.com")
        st.write("- Geoffrey Muchunguzi, Email: geoffreymuchunguzi@gmail.com")
        st.write("We appreciate their dedication and creativity in making this app extraordinary!")
