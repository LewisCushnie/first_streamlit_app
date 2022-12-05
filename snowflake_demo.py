import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
from connection import init_connection, run_query

conn = init_connection()

#============================= PAGE STARTS =================================

streamlit_credits_used = run_query(
'''select
sum(credits_used_cloud_services)
from query_history
where query_tag = 'StreamlitQuery';'''
)
streamlit_credits_used_df = pd.DataFrame(streamlit_credits_used, columns=['Streamlit_Credits_Used'])
st.write(streamlit_credits_used_df)

st.sidebar.header('Credits used in streamlit')
st.sidebar.metric("Credits used", streamlit_credits_used['Streamlit_Credits_Used'].values())

st.title('Snowflake Connectivity Demo')

all_RBAC_roles = run_query("select CREATED_ON, NAME, COMMENT, OWNER from roles;")
st.header("Roles Summary:")
st.dataframe(all_RBAC_roles)

metering_history = run_query("select name, credits_used from metering_history;")
st.header("Metering Summary:")
st.dataframe(metering_history)

databases = run_query("select * from databases;")
st.header("Databases:")
st.dataframe(databases)
