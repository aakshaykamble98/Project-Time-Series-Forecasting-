import numpy as np
import pickle
import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import warnings
warnings.filterwarnings("ignore") 

import base64


def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://www.shutterstock.com/image-vector/vector-illustration-abstract-electric-lightning-260nw-1706216764.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )


# Loading model
loaded_model = pickle.load(open(r"D:\ExcelR\Data Science\Project (Forecasting of energy consuption)\Ak Deployment\xg_model_values.pkl", 'rb'))


# Creating function for prediction

def energy_usage_pred(input_data):
    
    # input data as np array
    input_as_array = np.asarray(input_data)
    
    # reshape input  np array
    input_reshaped = input_as_array.reshape(1,-1)
    
    # Predict output
    predicted_output = loaded_model.predict(input_reshaped)
    
    return predicted_output
        

def main():
    
    set_bg_hack_url()  # Add this line to set the background image
    
    st.title('Energy Usage Forecast App')
    st.subheader('Enter data to get forecasted value of energy usage.')
    
    selection = st.selectbox('What type of forecast do you want?', ('Forecast for specific date and time', "Forecast for next 'n' days"))
    
    a = 'Forecast for specific date and time'
    b = "Forecast for next 'n' days"
    
    if selection == a:
    
        # Getting input from user
        Date = st.date_input('Enter the date. (YYYY/MM/DD) ')
        Time = st.time_input('Enter the time.')
        Hour = Time.hour
        Day = Date.day
        Month = Date.month
        # Quarter value
        if Month in (1,2,3):
            Quarter = 1
        elif Month in (4,5,6):
            Quarter = 2
        elif Month in (7,8,9):
            Quarter = 3
        else:
            Quarter = 4
        Year = Date.year
    
        # Code for forecast
        forecast = ''
        
        if st.button('Forecast'):
            forecast = energy_usage_pred([Hour, Day, Month, Quarter, Year])
            
        st.write(forecast)
    
    if selection == b:
        
        Date = st.date_input('Enter the date.')
        Time = st.time_input('Enter the time.')
        datetime_str = str(Date) + ' ' + str(Time)
        date_format = '%Y-%m-%d %H:%M:%S'
        datetime_object = datetime.strptime(datetime_str, date_format)
        
        Days = st.slider('Days for forecast', min_value=0, max_value=100, value=30)
        
        index_of_forecast = pd.date_range(datetime_object + pd.DateOffset(days=0), periods = Days*24, freq='H')
        
        fut_in = pd.DataFrame(index=index_of_forecast)
        fut_in['Hour'] = fut_in.index.hour
        fut_in['Day'] = fut_in.index.day
        fut_in['Month'] = fut_in.index.month
        fut_in['Quarter'] = fut_in.index.quarter
        fut_in['Year'] = fut_in.index.year
        
        forecast = loaded_model.predict(fut_in)                                                                                                                                                       
        fut_in['Energy usage (in MW)'] = forecast
        st.write('Dataframe with Forecast')
        fut_in
        
        # Generate a link to download the predicted data
        csv_file = fut_in.to_csv(index=False)
        b64 = base64.b64encode(csv_file.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="energy_forecast.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)


        st.write('Plotting of Forecasted Energy usage (in MW) VS Datetime')
        st.line_chart(data=fut_in['Energy usage (in MW)'])
        

if __name__ == '__main__':
    main()  