import streamlit as st
import pandas as pd
import pickle
import numpy as np

data = pd.read_csv("/home/siddesh/Desktop/Git_Repositories/Property_Price_Analysis_and_Prediction/data/gurgaon_properties_post_feature_selection_top_12.csv")

st.title("Gurgaon Property Price Predictor")


st.subheader("Please provide the below details to get a property price estimate")

#flat	sector 36	0.82	3	2	2	New Property	850	0	0	0	0	2

#Numeric columns
bedroom = st.number_input("Number of bedrooms", value=1, min_value=1, step=1)
bathroom = st.number_input("Number of bathrooms", value=1, min_value=1, step=1)
built_up_area = st.number_input("Built up area (in sq. ft.)", min_value=10, value=400, step=1)
study_room = st.number_input("Number of study rooms", value=0, min_value=0, step=1)
servant_room = st.number_input("Number of servant rooms", value=0, min_value=0, step=1)
store_room = st.number_input("Number of store rooms", value=0, min_value=0, step=1)
pooja_room = st.number_input("Number of pooja rooms", value=0, min_value=0, step=1)

#categorical columns
property_type = st.selectbox("Type of property", data['property_type'].unique())
sector = st.selectbox("Sector number", data['sector'].unique())
balcony = st.selectbox("Number of Balconies", data['balcony'].unique())
agePossession = st.selectbox("Age of the property", data['agePossession'].unique())
furnishing_type = st.selectbox("Furnishing of the property", ['Furnished', 'Semi Furnished', 'Unfurnished'])

if furnishing_type=='Furnished':
    furnishing_type=2
if furnishing_type=='Semi Furnished':
    furnishing_type=1
if furnishing_type=='Unfurnished':
    furnishing_type=0

col1, col2, col3 , col4, col5 = st.columns(5)

with col1:
    pass
with col2:
    pass
with col4:
    pass
with col5:
    pass
with col3 :
    btn = st.button("Get price estimate")

if btn:
    dummy_df = pd.DataFrame(data={'property_type':[property_type], 'sector':[sector], 'bedRoom':[bedroom],'bathroom':[bathroom],	'balcony':[balcony],'agePossession':[agePossession], 'built_up_area':[built_up_area],'study room':[study_room],'servant room':[servant_room],'store room':[store_room], 'pooja room':[pooja_room], 'furnishing_type':[furnishing_type]})
    with open("/home/siddesh/Desktop/Git_Repositories/Property_Price_Analysis_and_Prediction/model/final_model.pkl", 'rb') as model_file:
        pipeline = pickle.load(model_file)

    pred_value = np.expm1(pipeline.predict(dummy_df))
    print(f"prediction is {pred_value}")
    st.balloons()
    st.success(f"The expected price of the property would be in the range {(pred_value[0]-0.1).round(2)} Cr. and {(pred_value[0]+0.1).round(2)} Cr.")