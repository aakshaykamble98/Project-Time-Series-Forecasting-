import numpy as np
import pickle
import streamlit as st
import pandas as pd
from datetime import datetime


page_bg_img = '''
<style>
.stApp {
background-image: url("https://images.pexels.com/photos/923953/pexels-photo-923953.jpeg?cs=srgb&dl=light-dawn-landscape-923953.jpg&fm=jpg");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)


# Loading model
loaded_model = pickle.load(open(r"C:\Users\rohit\Python Project\Project\Energy usage Forecast.pkl", 'rb'))


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
    
    title = '<p style="font-family:sans-serif; color:darkblue; font-size: 45px; text-align:center; ">Energy Consumption Forecast App</p>'
    st.markdown(title, unsafe_allow_html=True)
    
    subtitle = '<p style="font-family:sans-serif; color:black; font-size: 25px; ">Enter data to get forecasted value of energy consumption.</p>'
    st.markdown(subtitle, unsafe_allow_html=True)
    
    selection = st.selectbox('What type of forecast do you want?', (None, 'Forecast for specific date and time', 
                                                                    "Forecast for next 'n' days from selected date",
                                                                    "Forecast using CSV file"))
    
    a = 'Forecast for specific date and time'
    b = "Forecast for next 'n' days from selected date"
    c = "Forecast using CSV file"
    
    if selection == None:
        warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">You haven't selected your preference for forecast.</p>"""
        st.markdown(warn, unsafe_allow_html=True)
    
    if selection == a:
    
        # Getting input from user
        Date = st.date_input('Enter the date. (YYYY/MM/DD) ')
        Time = st.time_input('Enter the time.', step=3600)
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
            st.write('Energy consumption for ', Date, 'and ', Time, 'is :',)
            forecast = energy_usage_pred([Hour, Day, Month, Quarter, Year])
            
               
    
    if selection == b:
        
        Date = st.date_input('Enter the date.')
        Time = st.time_input('Enter the time.', step=3600)
        datetime_str = str(Date) + ' ' + str(Time)
        date_format = '%Y-%m-%d %H:%M:%S'
        datetime_object = datetime.strptime(datetime_str, date_format)
        
        Days = st.number_input('Days for forecast', min_value=1)
        
        
        index_of_forecast = pd.date_range(datetime_object + pd.DateOffset(days=0), periods = Days*24, freq='H')
        
        fut_in = pd.DataFrame(index=index_of_forecast)
        fut_in['Hour'] = fut_in.index.hour
        fut_in['Day'] = fut_in.index.day
        fut_in['Month'] = fut_in.index.month
        fut_in['Quarter'] = fut_in.index.quarter
        fut_in['Year'] = fut_in.index.year
        
        
        forecast = loaded_model.predict(fut_in)
        fut_in['Energy consumption (in MW)'] = forecast
        st.write('Dataframe with Forecast :')
        
        
        selection1 = st.selectbox('Groupby :', ('Hour', 'Day', 'Month', 'Quarter', 'Year'))
        if selection1 == 'Hour':
            fut_in
            
            st.write('Plotting Forecasted Energy Consumption (in MW) VS Datetime : ' )
            st.line_chart(data=fut_in['Energy consumption (in MW)'])
            
        if selection1 == 'Day':
            fut_in = fut_in.groupby(fut_in['Day'])['Energy consumption (in MW)'].sum()
            fut_in = pd.DataFrame(fut_in, index=fut_in.index)
            fut_in
            
            st.write('Plotting Forecasted Energy Consumption (in MW) VS Day : ' )
            st.line_chart(data=fut_in['Energy consumption (in MW)'])
        
        if selection1 == 'Month':
            fut_in = fut_in.groupby(fut_in['Month'])['Energy consumption (in MW)'].sum()
            fut_in = pd.DataFrame(fut_in, index=fut_in.index)
            fut_in
            
            if Days > 35:
                st.write('Plotting Forecasted Energy Consumption (in MW) VS Month : ' )
                st.line_chart(data=fut_in['Energy consumption (in MW)'])
            else:
                warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">For plot, Days should be more than 35.</p>"""
                st.markdown(warn, unsafe_allow_html=True)
        
        if selection1 == 'Quarter':
            fut_in = fut_in.groupby(fut_in['Quarter'])['Energy consumption (in MW)'].sum()
            fut_in = pd.DataFrame(fut_in, index=fut_in.index)
            fut_in
            
            if Days > 90:
                st.write('Plotting Forecasted Energy Consumption (in MW) VS Quarter : ' )
                st.line_chart(data=fut_in['Energy consumption (in MW)'])
            else:
                warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">For plot, Days should be more than 90.</p>"""
                st.markdown(warn, unsafe_allow_html=True)
        
        if selection1 == 'Year':
            fut_in = fut_in.groupby(fut_in['Year'])['Energy consumption (in MW)'].sum()
            fut_in = pd.DataFrame(fut_in, index=fut_in.index)
            fut_in
            
            if Days > 365:
                st.write('Plotting Forecasted Energy Consumption (in MW) VS Year : ' )
                st.line_chart(data=fut_in['Energy consumption (in MW)'])
            else:
                warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">For plot, Days should be more than 365.</p>"""
                st.markdown(warn, unsafe_allow_html=True)
        
        
        # Downloading CSV file
        @st.cache_data
        def convert_df(df): 
            return df.to_csv().encode('utf-8')

        csv = convert_df(fut_in)

        st.download_button(
            label="Download data as CSV file :arrow_down:",
            data=csv,
            file_name='Fut_out.csv',
            mime='csv',)

      
    if selection == c:
        
        st.write('The CSV file should have format as follows :')
        info = """<p style="font-family:sans-serif; color:black; font-size: 15px; ">Column 1 : Datetime , Column 2 : Hour, Column 3 : Day, Column 4 : Month, Column 5 : Quarter, Column 6 : Year</p>"""
        st.markdown(info, unsafe_allow_html=True)
        uploaded_file = st.file_uploader('Choose CSV file')
        
        if uploaded_file is not None:
            Input = pd.read_csv(uploaded_file, index_col=0)
            st.write('Your uploaded file is :')
            st.write(Input)
            
            forecast = loaded_model.predict(Input)
            Input['Energy consumption (in MW)'] = forecast
            st.write('Dataframe with Forecast :')
            
            Days = len(Input['Day'])
            
            selection1 = st.selectbox('Groupby :', ('Hour', 'Day', 'Month', 'Quarter', 'Year'))
            if selection1 == 'Hour':
                Input
                
                st.write('Plotting Forecasted Energy Consumption (in MW) VS Datetime : ' )
                st.line_chart(data=Input['Energy consumption (in MW)'])
                
            elif selection1 == 'Day':
                Input = Input.groupby(Input['Day'])['Energy consumption (in MW)'].sum()
                Input = pd.DataFrame(Input, index=Input.index)
                Input
                
                st.write('Plotting Forecasted Energy Consumption (in MW) VS Day : ' )
                st.line_chart(data=Input['Energy consumption (in MW)'])
            
            elif selection1 == 'Month':
                Input = Input.groupby(Input['Month'])['Energy consumption (in MW)'].sum()
                Input = pd.DataFrame(Input, index=Input.index)
                Input
                
                if Days > 35:
                    st.write('Plotting Forecasted Energy Consumption (in MW) VS Month : ' )
                    st.line_chart(data=Input['Energy consumption (in MW)'])
                else:
                    warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">For plot, Days should be more than 35.</p>"""
                    st.markdown(warn, unsafe_allow_html=True)
            
            elif selection1 == 'Quarter':
                Input = Input.groupby(Input['Quarter'])['Energy consumption (in MW)'].sum()
                Input = pd.DataFrame(Input, index=Input.index)
                Input
                
                if Days > 90:
                    st.write('Plotting Forecasted Energy Consumption (in MW) VS Quarter : ' )
                    st.line_chart(data=Input['Energy consumption (in MW)'])
                else:
                    warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">For plot, Days should be more than 90.</p>"""
                    st.markdown(warn, unsafe_allow_html=True)
            
            elif selection1 == 'Year':
                Input = Input.groupby(Input['Year'])['Energy consumption (in MW)'].sum()
                Input = pd.DataFrame(Input, index=Input.index)
                Input
                
                if Days > 365:
                    st.write('Plotting Forecasted Energy Consumption (in MW) VS Year : ' )
                    st.line_chart(data=Input['Energy consumption (in MW)'])
                else:
                    warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">For plot, Days should be more than 365.</p>"""
                    st.markdown(warn, unsafe_allow_html=True)
            
            
            @st.cache_data
            def convert_df(df): 
                return df.to_csv().encode('utf-8')

            csv = convert_df(Input)

            st.download_button(
                label="Download data as CSV file :arrow_down:",
                data=csv,
                file_name='Fut_out.csv',
                mime='csv',)
            
            
        else:
            warn = """<p style="font-family:sans-serif; color:Red; font-size: 15px; ">You have not uploaded CSV file</p>"""
            st.markdown(warn, unsafe_allow_html=True)
            
    st.write('')
    st.write('') 
    st.write('') 
    st.write('') 
    
    if st.button('About company'):
        warn = """<p style="font-family:sans-serif; color:black; font-size: 15px; ">PJM Interconnection LLC (PJM) is a regional transmission organization (RTO) in the United States. It is part of the Eastern Interconnection grid operating an electric transmission system.</p>"""
        st.markdown(warn, unsafe_allow_html=True)
        link = 'https://pjm.com/'
        st.write('You can visit us on :', link)
    
    if st.button('About Us'):
        warn = """<p style="font-family:sans-serif; color:black; font-size: 15px; ">Group 2 of project P219.</p>"""
        st.markdown(warn, unsafe_allow_html=True)
    
    if st.button('Contact'):
        mail = 'group2-p219@excelr.com'
        st.write('E-mail :', mail)
        warn = """<p style="font-family:sans-serif; color:black; font-size: 15px; ">Number = '+91-xxxxxxxxxx'</p>"""
        st.markdown(warn, unsafe_allow_html=True)
        

if __name__ == '__main__':
    main()
    
