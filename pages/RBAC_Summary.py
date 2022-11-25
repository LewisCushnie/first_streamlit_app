import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
import snowflake_demo as sd

st.title('RBAC Roles Summary')

all_RBAC_roles = sd.run_query("select * from roles;")
st.header("Roles Summary:")
st.dataframe(all_RBAC_roles)

# Stop streamlit from running past this point
st.stop()