import numpy as np
import pickle
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px


page_bg_img = '''
<style>
.stApp {
background-image: url("https://wallpaper.dog/large/5554645.jpg");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)


# Loading model
loaded_model = pickle.load(open(r"D:\ExcelR\Data Science\Project (Forecasting of energy consuption)\Group members work\Preshant deployment\deploy.pkl", 'rb'))


# Creating function for prediction

def energy_usage_pred(input_data):
    
    # input data as np array
    input_as_array = np.asarray(input_data)
    
    # reshape input  np array
    input_reshaped = input_as_array.reshape(1,-1)
    
    # Predict output
    predicted_output = loaded_model.predict(input_reshaped)
    predicted_output
        
def main():
    
    st.title('Energy Consumption Forecast ')
    st.subheader("Welcome to the energy consumption forecasting tool! To get started, please choose an option below and provide the required input to obtain a forecasted value of energy consumption. Let's begin!")
    
    # About buttons
    
    if st.button('Learn more'):
        st.write('PJM Interconnection LLC (PJM) is a regional transmission organization (RTO) in the United States. It is part of the Eastern Interconnection grid operating an electric transmission system serving all or parts of Delaware, Illinois, Indiana, Kentucky, Maryland, Michigan, New Jersey, North Carolina, Ohio, Pennsylvania, Tennessee, Virginia, West Virginia, and the District of Columbia.Track electricity usage forecast in real time across the region PJM Interconnection. Simple and easy to use now works with this app.')
  
    
    selection = st.selectbox('What type of forecast do you want?', (None, 'Forecast for specific date and time', 
                                                                    "Forecast for next 'n' days from selected date",
                                                                    "Forecast using CSV file"))
    
    a = 'Forecast for specific date and time'
    b = "Forecast for next 'n' days from selected date"
    c = "Forecast using CSV file"
    
    if selection == None:
        st.write("You haven't selected your preference for forecast:exclamation:")
    
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
        st.write('Dataframe with Forecast :')
        fut_in
        
        # Downloading CSV file
        @st.cache_data
        def convert_df(df): 
            return df.to_csv().encode('utf-8')

        csv = convert_df(fut_in)

        st.download_button(
            label="Download data as CSV file :arrow_down:",
            data=csv,
            file_name='Fut_out',
            mime='text/csv',)

        st.write('Plotting of Forecasted Energy Consumption (in MW) VS Datetime : ' )
        st.line_chart(data=fut_in['Energy usage (in MW)'])
        chart_data = fut_in.reset_index()
        st.write('Scatter plot of Forecasted Energy Consuption (in MW) VS Datetime ')
        scatter_chart_data = chart_data[['index', 'Energy usage (in MW)']]
        st.write(px.scatter(chart_data, x='index', y='Energy usage (in MW)', title='Forecasted Energy Usage'))
        st.write('Area Chart of Forecasted Energy Consumption (in MW) VS Datetime:')
        st.area_chart(data=fut_in['Energy usage (in MW)'])
       
        
    if selection == c:
        
        st.write('The CSV file should have format as follows :')
        st.write('Col1 : Datetime , Col2 : Hour, Col3 : Day, Col4 : Month, Col5 : Quarter, Col6 : Year')
        uploaded_file = st.file_uploader('Choose CSV file')
        
        if uploaded_file is not None:
            Input = pd.read_csv(uploaded_file, index_col=0)
            st.write('Your uploaded file is :')
            st.write(Input)
            
            forecast = loaded_model.predict(Input)
            Input['Energy usage (in MW)'] = forecast
            st.write('Dataframe with Forecast :')
            Input
            
            @st.cache_data
            def convert_df(df): 
                return df.to_csv().encode('utf-8')

            csv = convert_df(fut_in)

            st.download_button(
                label="Download data as CSV file :arrow_down:",
                data=csv,
                file_name='Fut_out',
                mime='text/csv',)
            
        else:
            st.write('You have not uploaded CSV file:exclamation:')
        
    
if __name__ == '__main__':
    main()
    
