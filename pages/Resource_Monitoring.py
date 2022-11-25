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

metering = run_query("select name, credits_used from metering_history;")
st.header("Metering:")
st.dataframe(metering, width=500)

st.header('Select Warehouse(s):')
df = pd.DataFrame(metering)

option = st.selectbox(
    'Which number do you like best?',
     df['0'])

'You selected: ', option

# Stop streamlit from running past this point
st.stop()