import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
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

    st.title('RBAC Roles Summary')

    all_RBAC_roles = run_query("select CREATED_ON, NAME, COMMENT, OWNER from roles;")
    st.header("Roles Summary:")
    st.dataframe(all_RBAC_roles)