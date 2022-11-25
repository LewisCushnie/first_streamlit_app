import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
from snowflake_demo import run_query

st.title('Resource Monitoring Summary')

all_RBAC_roles = run_query("select name, credits_used from metering_history;")
st.header("Metering:")
st.dataframe(all_RBAC_roles)

# Stop streamlit from running past this point
st.stop()