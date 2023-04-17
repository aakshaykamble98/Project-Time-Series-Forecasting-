# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 00:01:28 2023

@author: HP
"""

import streamlit as st
import pickle
import pandas as pd
from datetime import datetime

st.title('Forecasting Hourly Energy Consumption :chart_with_upwards_trend:')


model = open('xg_model_value.pkl','rb')
xg_model = pickle.load(model)

def predict(hour, month, year, Day):
    prediction= xg_model.predict([[hour, month, year, Day]])
    return prediction


def main():
    st.markdown('This is simple webapp for prediction of energy consumption :bar_chart:')
    datetime_str = '08/03/18 00:00:00'
    datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    print(datetime_object)
    index_of_forecast = pd.date_range(datetime_object + pd.DateOffset(days=1), 
                                      periods = 30*24, freq='H')
    index_of_forecast
    forecast_data = pd.DataFrame(index=index_of_forecast)
    forecast_data['hour'] = forecast_data.index.hour
    forecast_data['month'] =forecast_data.index.month
    forecast_data['year'] = forecast_data.index.year
    forecast_data['Day'] = forecast_data.index.dayforecast_data
    forecast_data
    forecast = xg_model.predict(forecast_data.values)
    forecast = pd.DataFrame(forecast, columns=['Forecast'], index=forecast_data.index)
    forecast
    if st.button('Predict'):
        result = predict(hour, month, year, Day)
        st.success('The Energy Consumption in megawatts is : {}'.format(result))


if __name__== '__main__':
    main()
    
    
    
   

    



