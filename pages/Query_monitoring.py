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
columns=['Database', 'Schema', 'Role', 'Session', 'User', 'Warehouse', 'Region', 'Time'])
transposed_session_variables_df = snowflake_session_variables_df.transpose()
st.sidebar.dataframe(transposed_session_variables_df)

#------------------------------- Main Page ----------------------------------- 

with open("pages/style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.title('Query Monitoring')

    most_expensive_queries = run_query(
    '''
    select top 10 query_id
    ,credits_used_cloud_services
    ,total_elapsed_time/60000 as minutes_to_complete
    ,query_type
    ,database_name
    ,query_tag
    from SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY order by credits_used_cloud_services desc;'''
    )

    # Convert to pandas dataframe
    most_expensive_queries_df = pd.DataFrame(most_expensive_queries, columns=['QUERY_ID','CREDITS_USED_CLOUD_SERVICES','MINUTES_TO_COMPLETE', 'QUERY_TYPE', 'DATABASE_NAME', 'QUERY_TAG'])
    #most_expensive_queries_df = most_expensive_queries_df.set_index('CREDITS_USED_CLOUD_SERVICES')
    most_expensive_queries_df['CREDITS_USED_CLOUD_SERVICES'] = most_expensive_queries_df['CREDITS_USED_CLOUD_SERVICES'].astype(float)
    most_expensive_queries_df['MINUTES_TO_COMPLETE'] = most_expensive_queries_df['MINUTES_TO_COMPLETE'].astype(float)
    st.header("Queries Summary:")
    st.dataframe(most_expensive_queries_df)

    st.header('most recent queries')
    most_recent_queries = run_query(
    '''
    select top 15 query_id
    ,query_text
    ,start_time
    ,query_tag
    from SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY order by start_time desc;'''
    )

    # Convert to pandas dataframe
    most_expensive_queries_df = pd.DataFrame(most_recent_queries, columns=['id','text','time', 'tag'])
    #most_expensive_queries_df = most_expensive_queries_df.set_index('CREDITS_USED_CLOUD_SERVICES')
    st.header("Queries Summary:")
    st.dataframe(most_expensive_queries_df)