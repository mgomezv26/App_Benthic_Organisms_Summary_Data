import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Environmental Niche Analysis 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    ## Environmental Niche Analysis
    In this app, you can:
    - View maps showing the distribution of species.
    - See summary statistics of species occurrences.
"""
)