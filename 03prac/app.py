# main
from base64 import b64encode

import streamlit as st

from utils.utils import chain_recommend_food, chain_recommend_wine

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

