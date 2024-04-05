import streamlit as st

# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# Streamlit set_page_config method has a 'initial_sidebar_state' argument that controls sidebar state.
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)

# Show title and description of the app.
st.title('Gurgaon Property Price Prediction and Analysis')

st.markdown('This website uses information collected from properties of various sectors of Gurgaon to provide a price estimate based on user reqirements and display some analytics about Gurgaon real estate market')
st.sidebar.markdown('Home page for website')

# Toggle sidebar state between 'expanded' and 'collapsed'.
#if st.button('Click to toggle sidebar state'):
#    st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
#    # Force an app rerun after switching the sidebar state.
#    st.experimental_rerun()
