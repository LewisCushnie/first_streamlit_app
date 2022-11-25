import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
from snowflake_demo import a


st.title('RBAC Roles Summary')
st.write(a)
#st.dataframe(all_RBAC_roles)

# Stop streamlit from running past this point
#st.stop()