# STREAMLIT CHEAT SHEET WITH WORKING FEATURES AND CODE

# imports
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import numpy as np

'''
IMPORTANT NOTE ON STREAMLIT'S Data flow
Streamlit's architecture allows you to write apps the same way you write plain Python scripts. 
To unlock this, Streamlit apps have a unique data flow: any time something must be updated 
on the screen, Streamlit reruns your entire Python script from top to bottom.
This can happen in two situations:

(1) Whenever you modify your app's source code.
(2) Whenever a user interacts with widgets in the app. For example, when dragging a slider, entering text in an input box, or clicking a button.
'''

# This library returns the error that is presented by a website/api when you put a wrong input
# e.g https://websitename/page/dhjfdjhdfhjfd would return '404 page not found'
from urllib.error import URLError

# main titles
st.title('This is how you add a title')
st.header('This is how you create a header')
st.text('This is how you add text')
st.text('--------------------------------------------------------------------')

# ----------------------------------------------------------------------------------
# WORKING WITH PANADAS DATAFRAMES 
# ----------------------------------------------------------------------------------
st.header('Reading a CSV into a dataframe')

# reading a csv into a df
fruit_df = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
fruit_df = fruit_df.set_index('Fruit')

# Display the raw df on page.
st.header('Raw dataframe')
st.dataframe(fruit_df)

# Filtering using a PICK LIST
st.header('Dataframe filtered using the pick list')
# Multiselect list
fruits_selected = st.multiselect("Pick some fruits:", list(fruit_df.index),['Avocado','Strawberries'])
# filter using panda's .loc
fruits_to_show = fruit_df.loc[fruits_selected]

# Display the filtered df on the page.
st.dataframe(fruits_to_show)

# ----------------------------------------------------------------------------------
# WORKING WITH APIS (AND JSON RESPONSE)
# ----------------------------------------------------------------------------------
st.header("Displaying information from an API response")

try:
  fruit_choice = st.text_input('What fruit would you like information about?')

  # if they haven't typed a fruit
  if not fruit_choice:
    st.error("Please type a fruit to start")

  # if they have typed a fruit  
  else:
    st.write('You entered ', fruit_choice)
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
    # Normalise json response
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # Output to screen as table
    st.dataframe(fruityvice_normalized)

# If the user types in a wrong input, this will return the error directly from the API
except URLError as e:
  st.error()

# NOTE, when working with booleans, no need to write if value == True, can instead write if value:
# likewise, rather than if value != true, can write if not value
# this also works for string/empty strings, lists/empty lists, etc.

# ----------------------------------------------------------------------------------
# st.map() FOR PLOTTING MAP DATA
# ----------------------------------------------------------------------------------

# Slider widget to change number of data points on map
select_box_options = pd.Series([10,20,30,40,50])
n_points = st.selectbox('Number of points', select_box_options) # 👈 SELECTBOX WIDGET
n_points = st.button('Number of points') # 👈 BUTTON WIDGET
n_points = st.slider('Number of points') # 👈 SLIDER WIDGET

# Generating points on a map based on coordinates
map_data = pd.DataFrame(
    np.random.randn(n_points, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

# plot the map
st.map(map_data)

# ----------------------------------------------------------------------------------
# ASSIGNING THE 'KEY' PARAMETER TO A WIDGET ALLOWS THE VARIABLE TO BE ACCESSED
# ----------------------------------------------------------------------------------
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name

st.stop()


