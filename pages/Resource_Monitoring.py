import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import numpy as np
from urllib.error import URLError
import altair as alt
#from utils import charts, gui, processing

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
metering_top_10_df = pd.DataFrame(metering_top_10, columns=['WH_Name', 'Credits Used'])
metering_top_10_df = metering_top_10_df.set_index('WH_Name')
metering_top_10_df['Credits Used'] = metering_top_10_df['Credits Used'].astype(float)
st.dataframe(metering_top_10_df, width= 500)

# Multiselect list
wh_selected = st.multiselect("Pick Warehouse:", list(metering_top_10_df.index),['COMPUTE_WH'])
# filter using panda's .loc
WH_to_show_df = metering_top_10_df.loc[wh_selected]

# Display the filtered df on the page.
#filtered_wh = st.dataframe(WH_to_show)

st.bar_chart(metering_top_10_df, height= 500)

st.text('Filtered Bar Chart')
st.bar_chart(WH_to_show_df, height= 500)

click = st.button('Snow baby!')

if click:
    st.snow()
    click = False

st.stop()

# Bar chart
bar_chart = charts.get_bar_chart(
    df=metering_top_10_df,
    date_column="X",
    value_column="Y",
)

st.altair_chart(bar_chart, use_container_width=True)

st.stop()

st.write(metering_top_10_df)
new_df = metering_top_10_df.set_index('Y', inplace=False)
st.bar_chart(new_df)

metering_top_10 = run_query("select top 10 name, sum(credits_used) from metering_history group by name;")
metering_top_10_df = pd.DataFrame(metering_top_10, columns=['X', 'Y'])
st.write(metering_top_10_df)
st.write(type(metering_top_10_df))
# chart_data2 = chart_data.set_index('X', inplace=True)
c = alt.Chart(metering_top_10_df).mark_bar().encode(
    x='X', 
    y='Y')
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