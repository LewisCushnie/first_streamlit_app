import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import numpy as np
from urllib.error import URLError
import altair as alt
from snowflake_demo import run_query

st.title('Snowflake Connectivity Demo')
all_RBAC_roles = run_query("select CREATED_ON, NAME, COMMENT, OWNER from roles;")
st.header("Roles Summary:")
st.dataframe(all_RBAC_roles)

