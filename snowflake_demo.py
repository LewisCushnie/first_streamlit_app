import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
from connection import init_connection, run_query

conn = init_connection()

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
st.sidebar.metric("Credits used", rounded_credits)

snowflake_session_variables_df = pd.DataFrame(snowflake_session_variables, 
columns=['Database', 'Schema', 'Role', 'Session', 'User', 'Warehouse', 'Region', 'Time'])
transposed = snowflake_session_variables_df.transpose()

st.write(snowflake_session_variables_df)



#------------------------------- SIDEBAR ----------------------------------- 

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
