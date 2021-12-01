'''
CLI - streamlit run <filename.py>
'''

import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import datetime

st.set_page_config(page_title='911 Calls Data -- edit')
st.header('911 Data Visualization Test -- edit')


### -- LOAD DATA  

csv_file = '911Calls/911.csv'
sheet_name = 'DATA'


df_total = pd.read_csv(csv_file)
df = df_total.copy()
df['department'] = df['title'].apply(lambda x: x.split(':')[0])
df['callReason'] = df['title'].apply(lambda x: x.split(':')[1])
df['callTime'] = df['desc'].apply(lambda x: x.split('@')[1][:9])
df['date'] = df['timeStamp'].apply(lambda x: x.split(' ')[0])
df.rename(columns={'twp':'township'}, inplace=True)
df.drop(['title','e','zip', 'timeStamp', 'desc'], axis=1, inplace=True)

pie_df = df.groupby('department').count()['callReason']


### -- SHOW DATAFRAME
st.subheader('Complete Dataframe -- edit')
st.dataframe(df_total)
st.subheader('Revised Dataframe -- edit')
st.dataframe(df)


### -- COLUMN LAYOUT TO DISPLAY PIECHART PLOT AND IMAGE SIDE BY SIDE

col1, col2 = st.columns(2)

with col1:
    pie_chart = px.pie(pie_df,
        title='911 Calls by Department',
        values='callReason',
        names=pie_df.index)
    st.plotly_chart(pie_chart, use_container_width=True)

with col2:
    image = Image.open('images/pie_chart.png')
    st.image(image,
        caption='Available at unDraw.co',
        width=600)



### -- MULTISELECTION TOOL

reason = df['callReason'].unique().tolist()
callReason = st.multiselect('Reason for Calling:', reason, default=reason)


### -- FILTER BASED ON SELECTION

mask = df['callReason'].isin(callReason)
num_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {num_of_result}*')


### -- GROUP DATA AFTER SELECTION

grouped = df[mask].groupby('township').count()['callReason']
grouped = grouped.reset_index()
grouped = grouped.rename(columns={'callReason':'callCount'})

bar_chart = px.bar(grouped,
                x='township',
                y='callCount',
                text='callCount',
                color_discrete_sequence = ['#F63366']*len(grouped),
                template= 'plotly_white')

st.plotly_chart(bar_chart,use_container_width=True)



### -- PLOT ACCIDENT LOCATION

df.rename(columns={'lng':'lon'}, inplace=True)

st.map(df, zoom=4)


### -- GROUP BY DATE INFO

col3, col4 = st.columns([1,7])

byDate = df.groupby('date').count()['department']
byDate = byDate.reset_index()
byDate = byDate.rename(columns={'department':'callCount'})

line_chart = px.line(byDate, x='date', y='callCount')

with col3:
    st.write(" ")
    st.markdown(f'*Daily Call Count:*')
    st.write(byDate, use_container_width=True)
    
with col4:
    st.plotly_chart(line_chart, use_container_width=True)
    




### -- GROUP BY TIME (HOUR)

col5, col6 = st.columns([7,1])

with col5:
    byHour = df['callTime'].apply(lambda hour: hour.split(':')[0])
    byHour = df.groupby(byHour).count()['department']
    byHour = byHour.iloc[1:-1]
    byHour = byHour.reset_index()
    byHour = byHour.rename(columns={'department':'callCount'})

    line_chart2 = px.line(byHour, x='callTime', y='callCount')
    st.plotly_chart(line_chart2, use_container_width=True)

with col6:
    st.write(" ")
    st.markdown(f'*Hourly Call Count:*')
    st.write(byHour, use_container_width=True)
