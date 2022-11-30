import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import numpy as np
from urllib.error import URLError
import altair as alt

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
metering_top_10 = run_query("select top 10 name, sum(credits_used) from metering_history group by name;")
metering_top_10_df = pd.DataFrame(metering_top_10, columns=['X', 'Y'])

st.write(metering_top_10_df)
new_df = metering_top_10_df.set_index('Y', inplace=False)
st.bar_chart(new_df)

chart_data = metering_top_10_df
#chart_data_index = metering_top_10_df.set_index('X', inplace=False)
c = alt.Chart(chart_data).mark_bar().encode(
    x='X', y='Y')
st.altair_chart(c, use_container_width=True)

source = pd.DataFrame({
    'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]
})

c2 = alt.Chart(source).mark_bar().encode(
    x='a',
    y='b'
)
st.altair_chart(c2, use_container_width=True)

st.stop()


chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

c = alt.Chart(chart_data).mark_circle().encode(
    x='b', y='a', size='c', color='c', tooltip=['a', 'b', 'c'])

st.altair_chart(c, use_container_width=True)

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