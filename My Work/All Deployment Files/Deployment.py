# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 00:01:28 2023

@author: HP
"""

import streamlit as st
import plotly.express as px
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import base64
import os
import warnings
warnings.filterwarnings(('ignore'))


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
             background: url("https://thumbs.dreamstime.com/z/transmission-line-sunset-clear-orange-sky-no-end-pylons-30912720.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )



st.title('Forecasting Hourly Energy Consumption :chart_with_upwards_trend:')


subtitle = '<p style="font-family:sans-serif; color:green; font-size: 25px; ">Enter data to get forecasted value of energy consumption.</p>'
st.markdown(subtitle, unsafe_allow_html=True)

# Base directory of the current script
base_dir = os.path.dirname(__file__)

# Construct the full path to the pickle file
pickle_file_path = os.path.join(base_dir, 'xg_model_values.pkl')

# Load the model from the pickle file
with open(pickle_file_path, 'rb') as load:
    model = pickle.load(load)

#Creating function for prediction

def prediction(input_data):
    
    # input data as np array
    input_as_array = np.asarray(input_data)
    
    # reshape input  np array
    input_reshaped = input_as_array.reshape(1,-1)
    
    # Predict output
    predicted_output = model.predict(input_reshaped)
    predicted_output
        
def main():
    set_bg_hack_url()
    
    st.subheader("Welcome to the Energy Consumption Forecasting Tool!.  Let's begin!")
    subtitle = '<p style="font-family:sans-serif; color:black; font-size: 17px; ">Enter data to get forecasted value of energy consumption: </p>'
    st.markdown(subtitle, unsafe_allow_html=True)
    
    #About buttons
    
    if st.button('Learn more'):
        st.write('PJM Interconnection LLC (PJM) is a Regional Transmission Organization (RTO) in the United States. It is part of the Eastern Interconnection grid operating an electric transmission system serving all or parts of Delaware, Illinois, Indiana, Kentucky, Maryland, Michigan, New Jersey, North Carolina, Ohio, Pennsylvania, Tennessee, Virginia, West Virginia, and the District of Columbia.Track electricity usage forecast in real time across the region PJM Interconnection. Simple and easy to use now works with this app.')
        link = 'https://pjm.com/'
        st.write('You can visit us on :', link)
    
    selection = st.sidebar.selectbox('What type of forecast do you want?', 
                             (None, 
                              'Forecast for specific date and time',
                              "Forecast for next 'n' days",
                              "Forecast using CSV file"))
    
    a = 'Forecast for specific date and time'
    b = "Forecast for next 'n' days"
    c= "Forecast using CSV file"
    
    if selection == None:
       warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">You haven't selected your preference for forecast!</p>"""
       st.markdown(warn, unsafe_allow_html=True)
    
    if selection == a:
    
        # Getting input from user
        Date = st.date_input('Enter the date. (YYYY/MM/DD) ')
        Time = st.time_input('Enter the time.')
        Hour = Time.hour
        Day = Date.day
        Month = Date.month
        Year = Date.year
    
        # Code for forecast
        forecast = ''
        
        if st.button('Forecast'):
            st.write('Energy consumption for ', Date, 'and ', Time, 'is :',)
            forecast = prediction([Hour, Day, Month, Year])
        
    
    if selection == b:
        
        Date = st.date_input('Enter the date.')
        Time = st.time_input('Enter the time.')
        datetime_str = str(Date) + ' ' + str(Time)
        date_format = '%Y-%m-%d %H:%M:%S'
        datetime_object = datetime.strptime(datetime_str, date_format)
        
        Days = st.number_input('Days for forecast', min_value=1)
        
        index_of_forecast = pd.date_range(datetime_object + pd.DateOffset(days=0), periods = Days*24, freq='H')
        
        fut_in = pd.DataFrame(index=index_of_forecast)
        fut_in['Hour'] = fut_in.index.hour
        fut_in['Day'] = fut_in.index.day
        fut_in['Month'] = fut_in.index.month
        fut_in['Year'] = fut_in.index.year
        
        forecast = model.predict(fut_in)
        fut_in['Energy consumption (in MW)'] = forecast
        st.write('Dataframe with Forecast')
        
        selection_1 = st.selectbox('Groupby :', ('Hour', 'Day', 'Month', 'Year'))
        if selection_1 == 'Hour':
            fut_in
            
            st.write('Plotting Forecasted Energy Consumption (in MW) VS Datetime : ' )
            st.line_chart(data=fut_in['Energy consumption (in MW)'])
            
            chart_data = fut_in.reset_index()
            st.write('Scatter plot of Forecasted Energy Consumption (in MW) VS Datetime ')
            scatter_chart_data = chart_data[['index', 'Energy consumption (in MW)']]
            st.write(px.scatter(scatter_chart_data, x='index', y='Energy consumption (in MW)', title='Forecasted Energy Consumption'))
            
            
            st.write('Area Chart of Forecasted Energy Consumption (in MW) VS Datetime:')
            st.area_chart(data=fut_in['Energy consumption (in MW)'])
            
        if selection_1 == 'Day':
             fut_in = fut_in.groupby(fut_in['Day'])['Energy consumption (in MW)'].sum()
             fut_in = pd.DataFrame(fut_in, index=fut_in.index)
             fut_in
             
             st.write('Plotting Forecasted Energy Consumption (in MW) VS Day : ' )
             st.line_chart(data=fut_in['Energy consumption (in MW)'])
            
            
             chart_data = fut_in.reset_index()
             chart_data = chart_data[['Day', 'Energy consumption (in MW)']]
             st.write(px.scatter(chart_data, x='Day', y='Energy consumption (in MW)', title='Forecasted Energy consomption'))
            
             st.write('Area Chart of Forecasted Energy Consumption (in MW) VS Datetime:')
             st.area_chart(data=fut_in['Energy consumption (in MW)'])
            
            
        if selection_1 == 'Month':
             fut_in = fut_in.groupby(fut_in['Month'])['Energy consumption (in MW)'].sum()
             fut_in = pd.DataFrame(fut_in, index=fut_in.index)
             fut_in
             
             if Days > 30:
                 st.write('Plotting Forecasted Energy Consumption (in MW) VS Month : ' )
                 st.line_chart(data=fut_in['Energy consumption (in MW)'])
                 
                 chart_data = fut_in.reset_index()
                 st.write('Scatter plot of Forecasted Energy Consumption (in MW) VS Datetime ')
                 scatter_chart_data = chart_data[['Month', 'Energy consumption (in MW)']]
                 st.write(px.scatter(scatter_chart_data, x='Month', y='Energy consumption (in MW)', title='Forecasted Energy Consumption'))
                 
                 
                 st.write('Area Chart of Forecasted Energy Consumption (in MW) VS Datetime:')
                 st.area_chart(data=fut_in['Energy consumption (in MW)'])
                 
             else:
                 warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">For plot, Days should be more than 35!</p>"""
                 st.markdown(warn, unsafe_allow_html=True)
         
         
        if selection_1 == 'Year':
             fut_in = fut_in.groupby(fut_in['Year'])['Energy consumption (in MW)'].sum()
             fut_in = pd.DataFrame(fut_in, index=fut_in.index)
             fut_in
             
             if Days > 365:
                 st.write('Plotting Forecasted Energy Consumption (in MW) VS Year : ' )
                 st.line_chart(data=fut_in['Energy consumption (in MW)'])
                 
                 chart_data = fut_in.reset_index()
                 st.write('Scatter plot of Forecasted Energy Consumption (in MW) VS Datetime ')
                 scatter_chart_data = chart_data[['Year', 'Energy consumption (in MW)']]
                 st.write(px.scatter(scatter_chart_data, x='Year', y='Energy consumption (in MW)', title='Forecasted Energy Consumption'))
                 
                 
                 st.write('Area Chart of Forecasted Energy Consumption (in MW) VS Datetime:')
                 st.area_chart(data=fut_in['Energy consumption (in MW)'])
                 
             else:
                 warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">For plot, Days should be more than 365!</p>"""
                 st.markdown(warn, unsafe_allow_html=True)
        
        #Generate a link to download the predicted data
        csv_file = fut_in.to_csv(index=True)
        b64 = base64.b64encode(csv_file.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="Energy_forecasted.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)


    if selection == c:
            
        st.write('The CSV file should have format as follows :')
        st.write('Column 1 : Datetime , Column 2 : Hour, Column 3 : Day, Column 4 : Month, Column 5 : Year')
        uploaded_file = st.file_uploader('Choose CSV file')
            
        if uploaded_file is not None:
            Input = pd.read_csv(uploaded_file, index_col=0)
            st.write('Your uploaded file is :')
            st.write(Input)
                
            forecast = model.predict(Input)
            Input['Energy consumption (in MW)'] = forecast
            st.write('Dataframe with Forecast :')
            
            Days = len(Input['Day'])
            
            selection_1 = st.selectbox('Groupby :', ('Hour', 'Day', 'Month', 'Year'))
            if selection_1 == 'Hour':
                Input
                
                st.write('Plotting Forecasted Energy Consumption (in MW) VS Datetime : ' )
                st.line_chart(data=Input['Energy consumption (in MW)'])
                
                data = Input.reset_index()
                st.write('Scatter plot of Forecasted Energy Consumption (in MW) VS Datetime ')
                scatter_chart = data[['index', 'Energy consumption (in MW)']]
                st.write(px.scatter(scatter_chart, x='index', y='Energy consumption (in MW)', title='Forecasted Energy Consumption'))
                
                
                st.write('Area Chart of Forecasted Energy Consumption (in MW) VS Datetime:')
                st.area_chart(data=Input['Energy consumption (in MW)'])
                
                
            elif selection_1 == 'Day':
                Input = Input.groupby(Input['Day'])['Energy consumption (in MW)'].sum()
                Input = pd.DataFrame(Input, index=Input.index)
                Input
                
                st.write('Plotting Forecasted Energy Consumption (in MW) VS Day : ' )
                st.line_chart(data=Input['Energy consumption (in MW)'])
                
                data = Input.reset_index()
                st.write('Scatter plot of Forecasted Energy Consumption (in MW) VS Datetime ')
                scatter_chart = data[['Day', 'Energy consumption (in MW)']]
                st.write(px.scatter(scatter_chart, x='Day', y='Energy consumption (in MW)', title='Forecasted Energy Consumption'))
                
                
                st.write('Area Chart of Forecasted Energy Consumption (in MW) VS Datetime:')
                st.area_chart(data=Input['Energy consumption (in MW)'])
                
            
            elif selection_1 == 'Month':
                Input = Input.groupby(Input['Month'])['Energy consumption (in MW)'].sum()
                Input = pd.DataFrame(Input, index=Input.index)
                Input
                
                if Days > 30:
                    st.write('Plotting Forecasted Energy Consumption (in MW) VS Month : ' )
                    st.line_chart(data=Input['Energy consumption (in MW)'])
                    
                    data = Input.reset_index()
                    st.write('Scatter plot of Forecasted Energy Consumption (in MW) VS Datetime ')
                    scatter_chart = data[['Month', 'Energy consumption (in MW)']]
                    st.write(px.scatter(scatter_chart, x='Month', y='Energy consumption (in MW)', title='Forecasted Energy Consumption'))
                    
                    
                    st.write('Area Chart of Forecasted Energy Consumption (in MW) VS Datetime:')
                    st.area_chart(data=Input['Energy consumption (in MW)'])
                    
                else:
                    warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">For plot, Days should be more than 35!</p>"""
                    st.markdown(warn, unsafe_allow_html=True)
            
            
            elif selection_1 == 'Year':
                Input = Input.groupby(Input['Year'])['Energy consumption (in MW)'].sum()
                Input = pd.DataFrame(Input, index=Input.index)
                Input
                
                if Days > 365:
                    st.write('Plotting Forecasted Energy Consumption (in MW) VS Year : ' )
                    st.line_chart(data=Input['Energy consumption (in MW)'])
                    
                    data = Input.reset_index()
                    st.write('Scatter plot of Forecasted Energy Consumption (in MW) VS Datetime ')
                    scatter_chart = data[['Year', 'Energy consumption (in MW)']]
                    st.write(px.scatter(scatter_chart, x='Year', y='Energy consumption (in MW)', title='Forecasted Energy Consumptione'))
                    
                    
                    st.write('Area Chart of Forecasted Energy Consumption (in MW) VS Datetime:')
                    st.area_chart(data=Input['Energy consumption (in MW)'])
                    
                else:
                    warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">For plot, Days should be more than 365!</p>"""
                    st.markdown(warn, unsafe_allow_html=True)
            
            
            #Generate a link to download the predicted data
            csv = Input.to_csv(index=True)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="Energy_forecasting.csv">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)
            
        
        else:
             warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">You have not uploaded CSV file!</p>"""
             st.markdown(warn, unsafe_allow_html=True) 
        
         
        

if __name__ == '__main__':
    main()


