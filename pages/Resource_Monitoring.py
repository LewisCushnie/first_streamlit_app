import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import numpy as np
from urllib.error import URLError
import altair as alt
from connection import init_connection, run_query

conn = st.session_state['conn']

#============================= PAGE STARTS =================================

#------------------------------- SIDEBAR ----------------------------------- 

st.sidebar.header('Snowflake session')

streamlit_credits_used = run_query(
'''select
sum(credits_used_cloud_services)
from query_history
where query_tag = 'StreamlitQuery';'''
)

snowflake_session_variables = run_query(
'''select current_database() 
,current_schema()
,current_role()
,current_session()
,current_user()
,current_warehouse()
,current_region()
,current_time();'''
)

streamlit_credits_used_df = pd.DataFrame(streamlit_credits_used, columns=['Streamlit_Credits_Used'])
credits = streamlit_credits_used_df.iloc[0]['Streamlit_Credits_Used']
rounded_credits = round(credits, 5)
st.sidebar.metric("Credits used from streamlit queries", rounded_credits)

snowflake_session_variables_df = pd.DataFrame(snowflake_session_variables, 
columns=['Database', 'Schema', 'Current role', 'Session ID', 'Current user', 'Warehouse', 'Region', 'Region time'])
transposed_session_variables_df = snowflake_session_variables_df.transpose().reset_index()
transposed_session_variables_df = transposed_session_variables_df.rename(columns={"index": "Session Parameter", 0: "Value"})
st.sidebar.dataframe(transposed_session_variables_df)

#------------------------------- SIDEBAR ----------------------------------- 

with open("pages/style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.title('Resource Monitoring Summary')

    st.text(
    '''
    This page provides a breakdown of the resource useage within the Snowflake account to better understand
    where and how credits are being consumed on the account. This will include a number of interactive charts,
    as well as recomendaions for parameter changes within snowflake that aim to maximise resourcse consumption
    efficiency.

    This page will look at:

    - Warehouse monitoring
    - Task monitoring
    - Snowpipe monitoring
    '''
    )

    st.header("Metering Summary:")

    metering_history = run_query("select name, credits_used from metering_history;")
    st.dataframe(metering_history)

    st.header('Warehouse credit usage')

    # Get top 10 warehouses with most credit usage
    metering_top_10 = run_query("select top 10 name, sum(credits_used) from metering_history group by name;")

    # Convert to pandas dataframe
    metering_top_10_df = pd.DataFrame(metering_top_10, columns=['WH_Name', 'Credits Used'])
    metering_top_10_df = metering_top_10_df.set_index('WH_Name')
    metering_top_10_df['Credits Used'] = metering_top_10_df['Credits Used'].astype(float)

    # Multiselect list
    wh_selected = st.multiselect("Pick Warehouse:", list(metering_top_10_df.index),['COMPUTE_WH', 'CADENS_WH', 'INTL_WH'])
    # filter using panda's .loc
    WH_to_show_df = metering_top_10_df.loc[wh_selected]

    # Display the filtered df on the page.
    st.bar_chart(WH_to_show_df, height= 500)

    st.text('On/Off grid')
    col1, col2, col3 = st.columns(3)
    col1.metric("COMPUTE_WH", metering_top_10_df.loc['COMPUTE_WH', 'Credits Used'], 10)
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

    click = st.button('Snow baby!')

    if click:
        st.snow()
        click = False

    st.stop()