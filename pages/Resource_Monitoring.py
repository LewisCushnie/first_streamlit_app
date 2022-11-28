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
metering_df = pd.DataFrame(metering, columns=['Name', 'Credits Used'])

st.header("Metering:")
st.dataframe(metering_df, width=500)

st.bar_chart(data=metering_df, width=500)

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])

st.bar_chart(chart_data)

st.header('Select Warehouse(s):')

metering_df = pd.DataFrame(metering, columns= ('WH_Name', 'Credits Used'))
option = st.selectbox(
    'Which number do you like best?',
     metering_df['WH_Name'])

'You selected: ', option

# Stop streamlit from running past this point
st.stop()