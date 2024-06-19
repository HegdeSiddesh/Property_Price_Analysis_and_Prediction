import streamlit as st
import pandas as pd
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from get_recommendation import fetchSimilar


st.set_page_config(
    page_title = "Apartment Recommendation",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Apartment Recommendation - Gurgaon")

with open('/home/siddesh/Desktop/Git_Repositories/Property_Price_Analysis_and_Prediction/model/apartment_names.pkl', 'rb') as file:
        apartment_names = pkl.load(file)
    


#facilities', 'price_details', 'location_advantage'
criteria = st.selectbox("Choose the criteria for recomending apartments", ['Apartments with similar facilities', 'Apartments of similar cost', 'Apartments in similar vicinity', 'Properties near specific location'])

def load_data(apartment, criteria):
    return fetchSimilar(apartment, criteria)

if criteria == 'Apartments with similar facilities':
    apartment_name = st.selectbox("Select apartment to get recommendation", apartment_names.to_list())
    result = load_data(apartment_name, 'facilities')
    st.dataframe(result)
elif criteria == 'Apartments of similar cost':
    apartment_name = st.selectbox("Select apartment to get recommendation", apartment_names.to_list())
    result = load_data(apartment_name, 'price_details')
    st.dataframe(result)
elif criteria == 'Apartments in similar vicinity':
    apartment_name = st.selectbox("Select apartment to get recommendation", apartment_names.to_list())
    result = load_data(apartment_name, 'location_advantage')
    st.dataframe(result)
elif criteria == 'Properties near specific location':
    #TODO : Get the location names and selectbox to take location name and distance
    #Get the apartments having this location and at lesst than than distance
    #Display the names
    with open('/home/siddesh/Desktop/Git_Repositories/Property_Price_Analysis_and_Prediction/model/location_distances.pkl', 'rb') as location_save_file:
        location_distances = pkl.load(location_save_file)
        #type(location_distances)
        locations = location_distances.columns.to_list()
        locations.remove('PropertyName')
        selected_loc = st.selectbox("Select the location to fetch nearby apartments", locations)
        selected_dist = st.number_input("Enter the maximum distance from selected location (km)", value=50, min_value=5, max_value=1000, step=5)
        distances = location_distances[['PropertyName',selected_loc]].loc[location_distances[selected_loc]<=selected_dist]
        st.dataframe(distances)
    

    