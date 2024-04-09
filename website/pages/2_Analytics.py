import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import seaborn as sns
import ast #To convert string repr of list to python list

#Reference : https://blog.streamlit.io/crafting-a-dashboard-app-in-python-using-streamlit/

st.set_page_config(
    page_title="Gurgaon Property Analysis Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

data = pd.read_csv("/home/siddesh/Desktop/Git_Repositories/Property_Price_Analysis_and_Prediction/website/gurgaon_properties_with_latlong.csv")

#This col is just to center align title
col_main = st.columns((10, 25,1), gap='small')

with col_main[1]:

    st.title("Gurgaon Property Analysis")

    st.markdown("This page displays some insights obtained from the property data of Gurgaon")

st.sidebar.markdown('Analysis of Gurgaon properties')

group_df = data.groupby(['sector']).mean(numeric_only=True)[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']]

#print(group_df)

#st.dataframe(data)

col = st.columns((10, 25,10), gap='medium')


with col[0]:
    st.markdown('#### Sectors sorted by built up area')

    st.dataframe(group_df.sort_values('built_up_area', ascending=False),
                 column_order=("sector", "built_up_area"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "sector": st.column_config.TextColumn(
                        "Sector",
                    ),
                    "built_up_area": st.column_config.ProgressColumn(
                        "Built up area",
                        format="%.2f",
                        min_value=0,
                        max_value=max(group_df.built_up_area),
                     )}
                 )
    
    #with st.expander('About', expanded=True):
    #    st.write('''
    #        - Data: [U.S. Census Bureau](<https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html>).
    #        - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
    #        - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
    #        ''')



with col[1]:
    st.markdown('#### Map with sector wise price and built up area info')

    #Choose colorscales from here : https://plotly.com/python/builtin-colorscales/
    fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area', zoom=11, size_max=25, mapbox_style='open-street-map', color_continuous_scale="Turbo", width=1500, height=700, hover_name=group_df.index)

    st.plotly_chart(fig, use_container_width=True)
    with st.expander('About', expanded=True):
        st.write('''
            - Circle size represents the built up area for that sector
            - Circle color represents the price per sqft in the sector
            ''')


with col[2]:
    st.markdown('#### Sectors sorted by price per sqft')

    st.dataframe(group_df.sort_values('price_per_sqft', ascending=False),
                 column_order=("sector", "price_per_sqft"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "sector": st.column_config.TextColumn(
                        "Sector",
                    ),
                    "price_per_sqft": st.column_config.ProgressColumn(
                        "Price per sqft",
                        format="%.2f",
                        min_value=0,
                        max_value=max(group_df.price_per_sqft),
                     )}
                 )
    
    #with st.expander('About', expanded=True):
    #    st.write('''
    #        - Data: [U.S. Census Bureau](<https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html>).
    #        - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
    #        - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
    #        ''')



#Wordcloud :
    #Collect all amneties per sector 
    #In streamlit, take sector name as option and display wordcloud for that sector
    #Keep extra option "All sectors" to display wordcloud over complete data

col_2 = st.columns((1, 25,1), gap='medium')

with col_2[1]:

    st.title ("Wordcloud of Amneties for Sectors")

    amneties_data = pd.read_csv('/home/siddesh/Desktop/Git_Repositories/Property_Price_Analysis_and_Prediction/data/gurgaon_properties_cleaned_v1.csv')

    #print(amneties_data['features'])

    all_amneties = []
    sector_amneties_mapper = {}

    for sector in amneties_data['sector'].unique():
        sector_amneties_mapper[sector] = []

    sector_amneties_mapper['All_Sectors'] = []

    def collect_amneties_data(row):
        #print(row['sector'])
        #print(row['features'])
        try:
            feats = ast.literal_eval(row['features'])
        except:
            feats = []
        sector_amneties_mapper[row['sector']].extend(feats)
        sector_amneties_mapper['All_Sectors'].extend(feats)

    amneties_data.apply(collect_amneties_data, axis=1)

    #for sector in amneties_data['sector'].unique():
    #    print(len(sector_amneties_mapper[sector]))

    get_amneties = st.selectbox('Choose sector to view amneties provided', sector_amneties_mapper.keys(), index = 0)

    #btn = st.button('View popular amneties!')

    #if btn:
        #st.ballons()
        
    wordcloud = WordCloud(width=800, height=400, max_font_size=70, max_words=100, background_color="white").generate(' '.join(sector_amneties_mapper[get_amneties]))
    fig, ax = plt.subplots(figsize=(50,25))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    #plt.show()
    st.pyplot(fig,use_container_width=True)

st.title('Price analysisi based on other variables')

col_3 = st.columns((10, 10,10), gap='medium')

with col_3[0]:
    data['bedRoom'] = data['bedRoom'].apply(pd.to_numeric)
    data_bedRoom = data[data['bedRoom'] <=4 ]
    
    st.markdown('### Price movement by BHK box plot')
    sectors_list = amneties_data['sector'].unique().tolist()
    sectors_list = ['All Sectors'] + sectors_list
    sector_name_bhk = st.selectbox('Choose sector to view price Boxplot for BHK', sectors_list, index = 0)

    if sector_name_bhk=='All Sectors':
        fig = px.box(data_bedRoom,  x = 'bedRoom', y = 'price')
    else:
        #st.dataframe(data_bedRoom[data_bedRoom['sector']==sector_name_bhk])
        fig = px.box(data_bedRoom[data_bedRoom['sector']==sector_name_bhk], x = 'bedRoom', y = 'price')
    st.plotly_chart(fig, use_container_width=True)

with col_3[1]:
    st.markdown('### Price movement by House/Flat Area')
    sectors_list = amneties_data['sector'].unique().tolist()
    sectors_list = ['All Sectors'] + sectors_list
    price_vs_area_1 = st.selectbox('Choose sector to view price movement graph by area', sectors_list, index = 0)
    price_vs_area_type = st.selectbox('Choose the type of property', ['Any', 'House', 'Flat'], index = 0)

    if price_vs_area_1 == 'All Sectors':
        if price_vs_area_type == 'Any':
            fig = px.scatter(data, y = 'price', x = 'built_up_area')
        else :
            fig = px.scatter(data.loc[data['property_type']==price_vs_area_type.lower()], y = 'price', x = 'built_up_area')
    
    else :
        if price_vs_area_type == 'Any':
            fig = px.scatter(data.loc[data['sector']==price_vs_area_1], y = 'price', x = 'built_up_area')
        else :
            fig = px.scatter(data.loc[data['property_type']==price_vs_area_type.lower()].loc[data['sector']==price_vs_area_1], y = 'price', x = 'built_up_area')
    

    st.plotly_chart(fig, use_container_width=True)


with col_3[2]:
    st.markdown('### Sector wise distribution of price for House and Flat')
    sectors_list = amneties_data['sector'].unique().tolist()
    sectors_list = ['All Sectors'] + sectors_list
    price_dist_sector = st.selectbox('Choose sector to view price distribution', sectors_list, index = 0)

    if price_dist_sector == 'All Sectors':
        fig3 = plt.figure(figsize = (15,10))
        sns.distplot(data[data['property_type'] =='house']['price'], label='House')
        sns.distplot(data[data['property_type'] =='flat']['price'], label='Flat')
        plt.legend()
    else:
        fig3 = plt.figure(figsize = (15,10))
        sns.distplot(data[(data['sector'] == price_dist_sector) & (data['property_type'] =='house')]['price'], label='House')
        sns.distplot(data[(data['sector'] == price_dist_sector) & (data['property_type'] =='flat')]['price'], label='Flat')
        plt.legend()

    st.pyplot(fig3)

col_4 = st.columns((1, 25,1), gap='medium')

with col_4[1]:

    data['bedRoom'] = data['bedRoom'].apply(pd.to_numeric).astype(int)
    st.markdown('### Sector wise BHK distribution Pie chart')
    sectors_list = amneties_data['sector'].unique().tolist()
    sectors_list = ['All Sectors'] + sectors_list
    pie_dist_sector = st.selectbox('Choose sector to view BHK Pie chart', sectors_list, index = 0)

    if pie_dist_sector == 'All Sectors':
        fig_5 = px.pie(data, names='bedRoom')
    else:
        fig_5 = px.pie(data[data['sector']==pie_dist_sector], names='bedRoom')
    
    st.plotly_chart(fig_5, use_container_width=True)


