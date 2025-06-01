import streamlit as st
import pandas as pd
import numpy as np

# Load and preprocess data
path = 'EbayCleanedDataSample.csv'
df = pd.read_csv(path)
df = df.drop(['Unnamed: 0', 'Item Number'], axis=1)

tabs = st.tabs(["Data"])  # Create tabs and store them in a list
data_tab = tabs[0]  
with data_tab:
    st.image("https://www.topuniversities.com/sites/default/files/styles/736x304/public/guides/lead-bg-images/file%20-%202024-07-23T150458.046.jpg.webp",
              width=1000)

st.header("Ebay Dataset Exploration")
st.text("                        ------ Lambert Li")
st.subheader('Pandas DataFrame')
st.write(df)

# Universal sorting controls
st.text("Sort Options")
sort_column = st.selectbox("Select values to sort all tables by:", options=df.columns)
sort_order = st.radio("Select Order:", options=["Ascending", "Descending"])
ascending = sort_order == "Ascending"

# Filter 1: By Price Range
st.subheader("Ebay Sales Filtered by Price Range")
min_price, max_price = float(df['Price'].min()), float(df['Price'].max())
price_range = st.slider('Select Price Range:', min_value=min_price, max_value=max_price, value=(min_price, max_price))
filtered_df_slider = df[(df['Price'] >= price_range[0]) & (df['Price'] <= price_range[1])]
filtered_df_slider = filtered_df_slider.sort_values(by=sort_column, ascending=ascending)
st.dataframe(filtered_df_slider)

# Filter 2: By Brand
st.subheader('Ebay Data Filtered by Brands')
brand_option = df["Brand"].unique()
brand_selection = st.multiselect('Select Brands:', options=brand_option, default=brand_option)
brand_filtered_df = df[df['Brand'].isin(brand_selection)]
brand_filtered_df = brand_filtered_df.sort_values(by=sort_column, ascending=ascending)
st.dataframe(brand_filtered_df)

# Filter 3: By Color and Screen Size
st.subheader('Ebay Data Filtered by Color and Screen Size')
color_option = df["Color"].unique()
size_option = df["Screen Size"].unique()

color_selection = st.multiselect("Select Colors:", options=color_option, default=[])
size_selection = st.multiselect("Select Screen Sizes:", options=size_option, default=[])

# Combine filters
size_color_filtered_df = df[
    (df["Color"].isin(color_selection)) | (df["Screen Size"].isin(size_selection))
]
size_color_filtered_df = size_color_filtered_df.sort_values(by=sort_column, ascending=ascending)
st.dataframe(size_color_filtered_df)


# Bar chart of different Screen sizes
st.subheader('Bar Chart Showing Count of Screen Sizes')

# Group the dataframe by 'Screen Size' and count the occurrences
screen_size_counts = df['Screen Size'].value_counts()

# Display the bar chart with screen size counts on the y-axis
st.bar_chart(screen_size_counts)

paragraph = '''This chart showcases that the most common computers that are on Ebay have screen sizes
of 14.0 inch and 15.6 in. Sizes of 13.3 in and 11.6 in are less common, but stil available and have 
marketability. We should consider creating a customer survey and potentially expand our 13.3 and 11.6 in
offering to the market as the competition is lower. It is also important to avoid uncommon screen 
dimensions, such as 13.4 and 13.1 in, where matching cases may not be available.'''

st.text(paragraph)

#Start of question 3
import plotly.express as px

st.subheader('Plotly Bubble Chart')

df.sort_values("Price", inplace=True)
df_reset = df.reset_index(drop=True)
df_reset = df_reset.reset_index()


price_fig = px.scatter(df_reset, 
                       x='index', 
                       y='Price', 
                       color='Brand', 
                       title="Price Distribution from Low to High")

# Display the plot
st.plotly_chart(price_fig)

average_price_simpletek = df.loc[df['Brand'] == 'Simpletek', 'Price'].mean()
std_simpletek = df.loc[df['Brand'] == 'Simpletek', 'Price'].std()
format_avg_simpletek = f"${average_price_simpletek:,.2f}"
format_std_simpletek = f"${std_simpletek:,.2f}"

average_price = df['Price'].mean()
std_price = df['Price'].std()
format_avg_price = f"${average_price:,.2f}"
format_std_price = f"${std_price:,.2f}"

# create column layout
col1, col2 = st.columns(2)
# display key metrics in column layout
with col1:
    st.metric(label="(Higest Priced Product) Average - Simpletek", value=format_avg_simpletek, delta=format_std_simpletek)
with col2:
    st.metric(label="Average Price (All Products)", value=format_avg_price, delta=format_std_price)

paragraph = '''This chart showcases a smooth upward trend of pricing data. Near 80 percent of products
are priced below $500, while the final 20 percent of product represent a steep jump between $550 
to $2000. The upward trend started near price range $620 - $1000, making this customer market 
a good spot to enter and increase product offering, as fewer similar products exist and 
customization and marketing could greatly increase sales. '''

st.text(paragraph)

# Generate another Plotly chart with user input

chart_type = st.radio('Select chart type:', ('Line Chart', 'Box Plot', 'Histogram', 'Pie Chart'))

if chart_type == "Line Chart":
    fig = px.line(df_reset, x='index',y='Price', color='GPU',
                  title='Ebay Price Line Chart')
    st.plotly_chart(fig)

elif chart_type == 'Box Plot':
    fig = px.box(df, x='Brand', y='Price',
    title='Ebay Price by Brand')
    st.plotly_chart(fig)

elif chart_type == 'Histogram':
    fig = px.histogram(df, x='Brand', y='Price',
    title='Ebay Price by Brand', histfunc='avg')
    st.plotly_chart(fig)

elif chart_type == 'Pie Chart':
    brand_count = df['Brand'].value_counts().reset_index()
    brand_count.columns = ['Brand', 'Count']  # Rename columns for clarity

    # Create the pie chart
    fig = px.pie(brand_count, values='Count', names='Brand', 
                 title='Ebay Brand Distribution')

    # Display the chart in Streamlit
    st.plotly_chart(fig)