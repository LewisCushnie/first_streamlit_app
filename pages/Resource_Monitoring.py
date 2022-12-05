import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import numpy as np
from urllib.error import URLError
import altair as alt
from connection import init_connection, run_query

conn = init_connection()

#============================= PAGE STARTS =================================

st.title('Resource Monitoring Summary')

# Get top 10 warehouses with most credit usage
metering_top_10 = run_query("select top 10 name, sum(credits_used) from metering_history group by name;")

# Convert to pandas dataframe
metering_top_10_df = pd.DataFrame(metering_top_10, columns=['WH_Name', 'Credits Used'])
metering_top_10_df = metering_top_10_df.set_index('WH_Name')
metering_top_10_df['Credits Used'] = metering_top_10_df['Credits Used'].astype(float)

st.header('Warehouse credit usage')

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