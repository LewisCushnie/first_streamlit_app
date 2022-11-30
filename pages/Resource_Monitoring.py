import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import numpy as np
from urllib.error import URLError

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

# Initialize snowflake connection object
conn = init_connection()

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
st.bar_chart(metering_df, y=metering_df['Credits Used'])
st.stop()

# Get top 10 warehouses credit usage
metering_top_10 = run_query("select top 10 name, sum(credits_used) from metering_history group by name;")
metering_top_10_df = pd.DataFrame(metering_top_10, columns=['index', 'Credits Used'])
credits_used = metering_top_10_df['Credits Used']
metering_top_10_df.reset_index(drop=True)

df = pd.DataFrame(np.random.randn(30,2),columns=['A','B'])

# Display the filtered df on the page
st.header('Metering_top_10')
st.dataframe(metering_top_10, width=500)
st.header('Metering_top_10_df')
st.dataframe(metering_top_10_df, width=500)

st.line_chart(metering_top_10_df)
st.bar_chart(df)

st.stop()

st.header('Select Warehouse(s):')

metering_df = pd.DataFrame(metering, columns= ('WH_Name', 'Credits Used'))
option = st.selectbox(
    'Which number do you like best?',
     metering_df['WH_Name'])

'You selected: ', option

# Stop streamlit from running past this point
st.stop()