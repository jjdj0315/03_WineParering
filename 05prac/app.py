import os

import streamlit as st
from dotenv import load_dotenv

from utils.utils import chain_recommend_food, chain_recommend_wine

load_dotenv()
os.environ["LANGSMITH_TRACING"] = "True"

st.title("Food and Wine Pairing")

pairing_type = st.radio("Choose Pairing Type", ("Food Pairing", "Wine Pairing"))

description = st.text_input("Description")

if st.button("Pair"):
    if pairing_type == "Food Pairing":
        chain = chain_recommend_food()
    else:
        chain = chain_recommend_wine()

    respone = chain.invoke({"query": description})
    st.write(respone)
