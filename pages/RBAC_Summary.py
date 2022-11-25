import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
from snowflake_demo import all_RBAC_roles

st.title('RBAC Roles Summary')
st.dataframe(all_RBAC_roles)

# Stop streamlit from running past this point
#st.stop()