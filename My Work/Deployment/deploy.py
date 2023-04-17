# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 00:01:28 2023

@author: HP
"""

import streamlit as st
import pickle

st.title('Forecasting Hourly Energy Consumption :chart_with_upwards_trend:')


load = open('xg_model.pkl','rb')
model = pickle.load(load)

def predict(hour, dayofweek, quarter, month, year, 
            dayofyear,dayofmonth, weekofyear):
    prediction= model.predict([[hour, dayofweek, quarter, month, year, 
                dayofyear,dayofmonth, weekofyear]])
    return prediction


def main():
    st.markdown('This is simple webapp for prediction of energy consumption :bar_chart:')
    hour = st.selectbox('Hour', (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24))
    dayofweek = st.selectbox('Day of week',(0,1,2,3,4,5,6))
    quarter = st.selectbox('Quarter',(1,2,3,4))
    month = st.number_input('Month',min_value=0, max_value=12)
    year = st.text_input('Year','Type here')
    dayofyear = st.number_input('Day of year',min_value=1, max_value=365)
    dayofmonth = st.number_input('Day of month', min_value=1, max_value=31)
    weekofyear = st.number_input('Week of the year', min_value=1, max_value=53)
    if st.button('Predict'):
        result = predict(hour, dayofweek, quarter, month, year, 
                    dayofyear,dayofmonth, weekofyear)
        st.success('The Energy Consumption in megawatts is : ${}'.format(result))


if __name__== '__main__':
    main()
    
    
    
   

    



