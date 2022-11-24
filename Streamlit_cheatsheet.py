# STREAMLIT CHEAT SHEET WITH WORKING FEATURES AND CODE

# imports
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import numpy as np
import time

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
st.header('Add and display a session variable using the key parameter')
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name


# ----------------------------------------------------------------------------------
# USE CHECKBOXES TO SHOW/HIDE INFO
# ----------------------------------------------------------------------------------
st.header('(1) Use a checkbox to show/hide information')
# if the checkbox is ticked > show the dataframe
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data

# ----------------------------------------------------------------------------------
# USE SELECTBOXES TO PROVIDE OPTIONS
# ----------------------------------------------------------------------------------
st.header('(2) Use a selectbox to provide options')
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option

# ----------------------------------------------------------------------------------
# USING SIDEBARS TO KEEP SOME OPTIONS OFF TO THE SIDE
# ----------------------------------------------------------------------------------
# Add a selectbox to the sidebar:
st.sidebar.header('THIS IS THE SIDEBAR AREA')

add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

# ----------------------------------------------------------------------------------
# USING COLUMNS TO ORGANISE WIDGETS
# ----------------------------------------------------------------------------------
st.header('Use columns to add widgets side by side')

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

# ----------------------------------------------------------------------------------
# ADDING A PROGRESS BAR FOR LONGER COMPUTATIONS
# ----------------------------------------------------------------------------------
st.header('Demo progress bar using time.sleep')
'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.01)

'...and now we\'re done!'

# ----------------------------------------------------------------------------------
# HASHING TO IMPROVE PERFORMANCE
# ----------------------------------------------------------------------------------
# https://docs.streamlit.io/library/advanced-features/caching

'''
When you mark a function with the @st.cache decorator, it tells Streamlit that whenever the function is called it needs to check a few things:

(1) The input parameters that you called the function with
(2) The value of any external variable used in the function
(3) The body of the function
(4) The body of any function used inside the cached function
(5) If this is the first time Streamlit has seen these four components with these exact values and in this exact combination and order, it 
runs the function and stores the result in a local cache. Then, next time the cached function is called, if none of these components 
changed, Streamlit will skip executing the function altogether and, instead, return the output previously stored in the cache.
'''

@st.cache  # 👈 This function will be cached
def my_slow_function(arg1, arg2):
    # Do something really slow in here!
    return the_output

from PIL import Image
image = Image.open('LEWIS_CUSHNIE.png')
st.image(image, caption='Picture of me!', width = 500)

st.stop()


