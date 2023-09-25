import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load your retail and wholesale datasets
df = pd.read_csv('../data/Clean_food.csv')
wholesale_df = pd.read_csv('../data/wholesale_prices.csv')  


# Define a function for the dashboard page
def dashboard_page():
    # DATA PREVIEW
    st.title('Data Preview')
    # Define the number of rows to display per page
    rows_per_page = 10

    # Create a page number selector
    page_number = st.number_input("Enter Page Number", min_value=1, value=1)

    # Calculate the start and end rows for the current page
    start_row = (page_number - 1) * rows_per_page
    end_row = start_row + rows_per_page

    # Display the DataFrame for the current page
    st.dataframe(wholesale_df.iloc[start_row:end_row])


    # PIE CHARTS
    # Create three columns for the pie charts
    head1, head3 = st.columns(2)
    with head1:
        st.markdown("<h1 style='text-align: center;'>Pie Chart of Price types</h1>", unsafe_allow_html=True)
    with head3:
        st.markdown("<h1 style='text-align: center;'>Pie Chart of Wholesale Commodities</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    # Create and display the first pie chart in col1
    with col1:
        price_type_counts = df['pricetype'].value_counts()
        explode = (0.1, 0.1)
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        ax1.pie(price_type_counts, labels=price_type_counts.index, autopct='%1.1f%%', startangle=90,
               explode=explode, shadow=True)
        ax1.axis('equal')
        st.pyplot(fig1)

    # Create and display the third pie chart in col3
    with col3:
        commodities2 = wholesale_df['commodity'].value_counts()
        explode = (0.1, 0.1, 0.05)
        fig3, ax3 = plt.subplots()
        ax3.pie(commodities2, labels=commodities2.index, autopct='%1.1f%%', startangle=90, explode=explode, shadow=True,
          pctdistance=0.85, wedgeprops=dict(width=0.4))
        circle = plt.Circle((0, 0), 0.6, fc='white')
        fig3.gca().add_artist(circle)
        ax3.axis('equal')
        st.pyplot(fig3)
    
    # MAPS (RETAIL AND WHOLESALE)
    # Create columns layout for the maps
    #map1_column, map2_column = st.columns(2)

    # Display the second map
    st.markdown("<h1 style='text-align: center;'>Map of Wholesale Market</h1>", unsafe_allow_html=True)
    st.write('This map shows the wholesale markets where data was collected. Our main focus was for wholesale markets.')
    st.map(wholesale_df[['latitude', 'longitude']])
    
    # BAR PLOT OF COMMODITIES IN YEARS
    st.title('Bar Plots of Commodities in various Years')
    # Get unique years in the dataset
    unique_years = wholesale_df['year'].unique()

    # Create a multiselect dropdown for selecting years
    selected_years = st.multiselect('Select Year(s)', unique_years)

    # Check if multiple years are selected
    if len(selected_years) > 1:
        # Display bar plots horizontally
        fig, axes = plt.subplots(1, len(selected_years), figsize=(16, 6))  # Adjust the figure size here
        for i, year in enumerate(selected_years):
            # Filter the data for the selected year
            filtered_data = wholesale_df[wholesale_df['year'] == year]

            # Create a bar plot for the selected year
            sns.barplot(x='commodity', y='price', data=filtered_data, palette='viridis', ci=None, ax=axes[i])
            axes[i].set_title(f'Commodities in {year}')
            axes[i].tick_params(axis='x', rotation=0)
            axes[i].set_xlabel('')
            axes[i].set_ylabel('Mean Price')

        # Adjust subplot spacing
        plt.tight_layout()
        st.pyplot(fig)
    else:
        # Display a single bar plot vertically
        if selected_years:
            selected_year = selected_years[0]
            filtered_data = wholesale_df[wholesale_df['year'] == selected_year]
            plt.figure(figsize=(3, 2))  # Adjust the figure size here
            sns.barplot(x='commodity', y='price', data=filtered_data, palette='viridis', ci=None)
            plt.title(f'Commodities in {selected_year}')
            plt.xticks(rotation=0)
            plt.xlabel('')
            plt.ylabel('Mean Price')
            st.pyplot(plt)


    # BARPLOT FOR COMPARING AVERAGE PRICES IN VARIOUS MARKETS 
    st.title("Average Price of Commodities by Market Comparison")

    # Multiselect widget for selecting multiple markets in col1
    selected_markets = st.multiselect("Select Markets:", wholesale_df["market"].unique())

    # Check if there are selected markets
    if not selected_markets:
        st.warning("Please select one or more markets for comparison.")
    else:
        # Filter data based on user-selected markets
        filtered_data = wholesale_df[wholesale_df["market"].isin(selected_markets)]

        # Create a bar chart to visualize the average price of other commodities by market
        plt.figure(figsize=(11, 5))
        sns.barplot(x='commodity', y='price', hue='market', data=filtered_data, ci=None)
        plt.xlabel('Commodity')
        plt.ylabel('Average Price')
        plt.title('Average Price of Other Commodities in Selected Markets')
        plt.xticks(rotation=0)
        plt.legend(title='Market')
        plt.show()

        # Display the bar chart in the Streamlit app
        st.pyplot(plt)

    # TIME SERIES (WHOLESALE)
    st.title('Time Series Analysis')

    ts1, ts2 = st.columns(2)

    # Sidebar: Allow the user to select a year or month
    with ts1:
        times_selection = st.selectbox('Select Year or Month', ['Year', 'Month'], key='times_selection_unique_key')

    # Sidebar: Allow the user to select commodities
    with ts2:
        selected_commodities = st.multiselect('Select Commodities', wholesale_df['commodity'].unique())

    # Filter the data based on selected year/month and commodities
    if times_selection == 'Year':
        times_column = 'year'
    else:
        times_column = 'month'

    filtered_data = wholesale_df[wholesale_df['commodity'].isin(selected_commodities)]

    # Create a time series plot to visualize price trends
    plt.figure(figsize=(8, 3))
    sns.lineplot(x=times_column, y='price', hue='commodity', data=filtered_data, marker='o')
    plt.xlabel(times_column)
    plt.ylabel('Price')
    #plt.title(f'Time Series Analysis of Selected Commodities Prices in Wholesale Markets ({time_selection})')
    plt.xticks(rotation=45)
    plt.legend(title='Commodity')
    plt.grid(True)

    # Display the plot in Streamlit
    st.pyplot(plt)

    # LINE PLOT OF MAX AND MIN (YEAR)
    # Group by "market", "commodity", and "year" to calculate max and min prices
    grouped_year = wholesale_df.groupby(["market", "commodity", "year"])["price"].agg(['max', 'min']).reset_index()

    # Create a Streamlit app
    st.title("Max and Min Prices by Year")

    # Define markets and commodities
    markets = grouped_year["market"].unique()
    commodities = grouped_year["commodity"].unique()

    # Create a container for the horizontal drop-down bars
    selection_container = st.empty()

    # Set up CSS for horizontal drop-down bars
    css = """
    .horizontal-dropdown-bar {
        display: flex;
        flex-direction: row;
    }
    .horizontal-dropdown-bar select {
        margin-right: 10px;
    }
    """
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # Create horizontal drop-down bars for market and commodity selection
    with selection_container.form(key='horizontal_dropdowns'):
        selected_market = st.selectbox("Select Market:", markets, key="market_dropdown")
        selected_commodity = st.selectbox("Select Commodity:", commodities, key="commodity_dropdown")
        st.form_submit_button(label='Submit')

    # Filter data based on user selection
    filtered_data = grouped_year[(grouped_year["market"] == selected_market) & (grouped_year["commodity"] == selected_commodity)]

    # Create line chart for max and min prices by year
    st.subheader(f"Max and Min Prices for {selected_commodity} in {selected_market} by Year")
    plt.figure(figsize=(10, 4))

    # Using seaborn for better styling
    sns.lineplot(data=filtered_data, x="year", y="max", label=f"Max Price", marker='o')
    sns.lineplot(data=filtered_data, x="year", y="min", label=f"Min Price", marker='o')

    plt.title(f"Max and Min Prices for {selected_commodity} in {selected_market} by Year")
    plt.xlabel("Year")
    plt.ylabel("Price")
    plt.legend(loc='upper left')
    plt.grid()

    st.pyplot(plt)

    #LINE PLOT FOR MAX AND MIN (MONTH)
    # Group by "market", "commodity", and "month" to calculate max and min prices
    grouped_month = wholesale_df.groupby(["market", "commodity", "month"])["price"].agg(['max', 'min']).reset_index()

    # Create a Streamlit app
    st.title("Max and Min Prices by Month")

    # Define markets and commodities
    markets = grouped_month["market"].unique()
    commodities = grouped_month["commodity"].unique()

    # Create a container for the horizontal drop-down bars
    selection_container = st.empty()

    # Set up CSS for horizontal drop-down bars
    css = """
    .horizontal-dropdown-bar {
        display: flex;
        flex-direction: row;
    }
    .horizontal-dropdown-bar select {
        margin-right: 10px;
    }
    """
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # Create horizontal drop-down bars for market and commodity selection
    with selection_container.form(key='Month_horizontal_dropdowns'):
        selected_market = st.selectbox("Select Market:", markets, key="Month_market_dropdown")
        selected_commodity = st.selectbox("Select Commodity:", commodities, key="Month_commodity_dropdown")
        st.form_submit_button(label='Submit')

    # Filter data based on user selection
    filtered_data = grouped_month[(grouped_month["market"] == selected_market) & (grouped_month["commodity"] == selected_commodity)]

    # Create line chart for max and min prices by year
    st.subheader(f"Max and Min Prices for {selected_commodity} in {selected_market} by Month")
    plt.figure(figsize=(10, 4))

    # Using seaborn for better styling
    sns.lineplot(data=filtered_data, x="month", y="max", label=f"Max Price", marker='o')
    sns.lineplot(data=filtered_data, x="month", y="min", label=f"Min Price", marker='o')

    plt.title(f"Max and Min Prices for {selected_commodity} in {selected_market} by Month")
    plt.xlabel("Month")
    plt.ylabel("Price")
    plt.legend(loc='upper left')
    plt.grid()

    st.pyplot(plt)

    st.markdown("---")

    # Create two columns for dLab information and development team credits
    coot1, coot2 = st.columns(2)

    # dLab Tanzania information
    with coot1:
        st.image('../images/dlab_logo.png', width=100)
        st.write("dLab Tanzania")
        st.write("Address Line: P. O. Box 33335, DSM")
        st.write("Email Address: connect@dlab.or.tz")
        st.write("Phone Number: 0225 222 410 645 / 0222 410 690")

    # Development team credits
    with coot2:
        st.markdown("### Development Team")
        st.write("Meet the talented individuals who made this app possible:")
        st.write("- Juma Omar, Email: jumaomar97@gmail.com")
        st.write("- Basilisa Katani, Email: lisakatani1008@gmail.com")
        st.write("- James Loma, Email: jamesloma80@gmail.com")
        st.write("- Geoffrey Muchunguzi, Email: geoffreymuchunguzi@gmail.com")
        st.write("We appreciate their dedication and creativity in making this app extraordinary!")