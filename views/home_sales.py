import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# set page configurations
st.set_page_config(
    page_title="Housing Market",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"  # 'collapsed' or 'expanded'
)

# set global dictionaries
county_fips = {
    'Habersham': '13137',
    'Banks': '13011'
}

# create tuple for filtering
fips_values = tuple(county_fips.values())

# create reverse dict from above
fips_county = {v: k for k, v in county_fips.items()}


@st.cache_data
def load_geometry():
    # Load the geometry data
    gdf = gpd.read_file('Data/blockGroups.gpkg')
    return gdf


@st.cache_data
def load_sales_data():
    # Load sales data & filter
    sales_df = gpd.read_file('Data/sales_file.csv')
    sales_df['BG_ID'] = sales_df['BG_ID'].astype(str)

    sales_df['square_footage'] = sales_df['square_footage'].astype(
        float).astype(int)
    sales_df['bedrooms'] = sales_df['bedrooms'].astype(
        float).astype(int)
    sales_df['bathrooms'] = sales_df['bathrooms'].astype(
        float)

    sales_df['price'] = sales_df['price'].astype(
        float)
    sales_df['price_sf'] = sales_df['price_sf'].astype(
        float)

    # make sure lat / long values are floats
    sales_df['latitude'] = sales_df['latitude'].astype(
        float)
    sales_df['longitude'] = sales_df['longitude'].astype(
        float)

    return sales_df


# "filter map by"
st.markdown('''
            <div style="display: flex; justify-content: center;"><p style="font-size: 20px;">Filter map by:</p></div>
            ''',
            unsafe_allow_html=True)

# define user input widgets
col1, col2, col3 = st.columns(3)
sf_select = col1.slider(
    "Home square footage",
    400,
    6000,
    (1000, 2500),
    step=100
)

bedroom_select = col2.slider(
    "Minimum number of bedrooms",
    0,
    6
)

bathroom_select = col3.slider(
    "Minimum number of bathrooms",
    0.0,
    6.0,
    step=0.5,
    format="%.1f"
)

map_variable = st.radio(
    label='Select map aggregation',
    options=['Total sales', 'Median price', 'Median home size'],
    index=0,
)

map_variable_switch = {
    'Total sales': 'total_sales',
    'Median price': 'median_price',
    'Median home size': 'median_SF'
}

# load sales data
sales_df = load_sales_data()

# load geometry
gdf = load_geometry()

# filter 1: home size
sales_df = sales_df[sales_df['square_footage'] >= sf_select[0]]
sales_df = sales_df[sales_df['square_footage'] <= sf_select[1]]

# filter 2: bedroom count
sales_df = sales_df[sales_df['bedrooms'] >= bedroom_select]

# filter 3: bathroom count
sales_df = sales_df[sales_df['bathrooms'] >= bathroom_select]

# create aggregation
sales_agg = sales_df.groupby('BG_ID').agg(
    total_sales=('address', 'count'),
    median_price=('price', 'median'),
    median_priceSF=('price_sf', 'median'),
    median_SF=('square_footage', 'median')
).reset_index()

# extract county name
sales_agg['county_name'] = sales_agg['BG_ID'].str[:5]
sales_agg['county_name'] = sales_agg['county_name'].map(fips_county)

merged_gdf = gdf.merge(
    sales_agg,
    left_on='GEOID',
    right_on='BG_ID'
).set_index('GEOID')

# st.dataframe(sales_agg, use_container_width=True)
st.write(merged_gdf)


# remove modebar
config = {'displayModeBar': False}


# the custom CSS lives here:
hide_default_format = """
        <style>
            .reportview-container .main footer {visibility: hidden;}    
            #MainMenu, footer {visibility: hidden;}
            [data-testid="stAppViewBlockContainer"] {
                padding-top: 50px;
                padding-left: 50px;
                padding-right: 60px;
                }
            [class="stAppDeployButton"] {
                display: none;
            } 
            div.stActionButton{visibility: hidden;}
        </style>
       """

# inject the CSS
st.markdown(hide_default_format, unsafe_allow_html=True)
