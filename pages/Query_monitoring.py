import streamlit as st
import pandas as pd
import requests
import snowflake.connector
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
st.title('Query Monitoring')

most_expensive_queries = run_query(
'''select top 10 credits_used_cloud_services
,query_type
,database_name
,total_elapsed_time/60000 as minutes_to_complete
from SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY order by credits_used_cloud_services desc;'''
)

# Convert to pandas dataframe
most_expensive_queries_df = pd.DataFrame(most_expensive_queries, columns=['CREDITS_USED_CLOUD_SERVICES', 'QUERY_TYPE', 'DATABASE_NAME', 'MINUTES_TO_COMPLETE'])
most_expensive_queries_df = most_expensive_queries_df.set_index('CREDITS_USED_CLOUD_SERVICES')
most_expensive_queries_df['Credits Used'] = most_expensive_queries_df['CREDITS_USED_CLOUD_SERVICES'].astype(float)
most_expensive_queries_df['Credits Used'] = most_expensive_queries_df['MINUTES_TO_COMPLETE'].astype(int)
st.header("Queries Summary:")
st.dataframe(most_expensive_queries_df)