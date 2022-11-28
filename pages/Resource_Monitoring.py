import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

# Funtion to perform queries from the database.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

#============================= PAGE STARTS =================================

st.title('Resource Monitoring Summary')

# Get all warehouses credit usage
metering = run_query("select name, credits_used from metering_history;")
metering_df = pd.DataFrame(metering, columns=['Name', 'Credits Used'])

# Get top 10 warehouses credit usage
# metering_top_10 = run_query("select top 10 name, credits_used from metering_history;")
# metering_top_10_df = pd.DataFrame(metering, columns=['Name', 'Credits Used'])

st.header("Metering:")
metering_selections = st.multiselect("Select Warehouses:", list(metering_df['Name'].index), ['INTL_WH','COMPUTE_WH'])
# filter using panda's .loc
fruits_to_show = metering_df.loc[metering_selections]

# Display the filtered df on the page
st.dataframe(metering_df, width=500)

# st.bar_chart(data=metering_top_10_df, width=500)

st.header('Select Warehouse(s):')

metering_df = pd.DataFrame(metering, columns= ('WH_Name', 'Credits Used'))
option = st.selectbox(
    'Which number do you like best?',
     metering_df['WH_Name'])

'You selected: ', option

# Stop streamlit from running past this point
st.stop()