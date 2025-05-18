# main
import os

import streamlit as st
from dotenv import load_dotenv

from utils.utils import chain_recommend_food, chain_recommend_wine

load_dotenv()
os.environ["LANGSMITH_TRACING"] = "False"


st.title("Food and Wine Pairing")

pairing_type = st.radio("choose Pairing Type", ("Food Pairing", "Wine Pairing"))

description = st.text_input("Description")


if st.button("Pair"):

    # Example processing (this is where the pairing logic would go)
    if pairing_type == "Food Pairing":
        chain = chain_recommend_food()
    else:
        chain = chain_recommend_wine()

    response = chain.invoke(
        {
            "query": description,
        }
    )
    st.write(response)
