# STREAMLIT CHEAT SHEET WITH WORKING FEATURES AND CODE

# imports
import streamlit
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
streamlit.title('This is how you add a title')
streamlit.header('This is how you create a header')
streamlit.text('This is how you add text')
streamlit.text('--------------------------------------------------------------------')

# ----------------------------------------------------------------------------------
# WORKING WITH PANADAS DATAFRAMES 
# ----------------------------------------------------------------------------------
streamlit.header('Reading a CSV into a dataframe')

# reading a csv into a df
fruit_df = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
fruit_df = fruit_df.set_index('Fruit')

# Display the raw df on page.
streamlit.header('Raw dataframe')
streamlit.dataframe(fruit_df)

# Filtering using a PICK LIST
streamlit.header('Dataframe filtered using the pick list')
# Multiselect list
fruits_selected = streamlit.multiselect("Pick some fruits:", list(fruit_df.index),['Avocado','Strawberries'])
# filter using panda's .loc
fruits_to_show = fruit_df.loc[fruits_selected]

# Display the filtered df on the page.
streamlit.dataframe(fruits_to_show)

# ----------------------------------------------------------------------------------
# WORKING WITH APIS (AND JSON RESPONSE)
# ----------------------------------------------------------------------------------
streamlit.header("Displaying information from an API response")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')

  # if they haven't typed a fruit
  if not fruit_choice:
    streamlit.error("Please type a fruit to start")

  # if they have typed a fruit  
  else:
    streamlit.write('You entered ', fruit_choice)
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
    # Normalise json response
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # Output to screen as table
    streamlit.dataframe(fruityvice_normalized)

# If the user types in a wrong input, this will return the error directly from the API
except URLError as e:
  streamlit.error()

# NOTE, when working with booleans, no need to write if value == True, can instead write if value:
# likewise, rather than if value != true, can write if not value
# this also works for string/empty strings, lists/empty lists, etc.

# ----------------------------------------------------------------------------------
# st.map() FOR PLOTTING MAP DATA
# ----------------------------------------------------------------------------------

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

streamlit.stop()


