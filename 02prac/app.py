# main
from base64 import b64encode

import streamlit as st

from utils.utils import chain_recommend_food, chain_recommend_wine

st.title("Food and Wine Pairing")

pairing_type = st.radio("choose Pairing Type", ("Food Pairing", "Wine Pairing"))

description = st.text_input("Description")

upload_type = st.radio(
    "Choose upload type: (Support formats: jpeg, jpg, gif, png)", ("Image", "URL")
)
if upload_type == "Image":
    # File uploader for attachment
    uploaded_file = st.file_uploader("Upload an attachment")
else:
    # Text input for image URL
    image_url = st.text_input("Image URL")

if st.button("Pair"):
    if upload_type == "Image" and uploaded_file is not None:
        base64_file = b64encode(uploaded_file.read()).decode("utf-8")
        image_urls = [f"data:image/png;base64,{base64_file}"]
    elif upload_type == "URL" and image_url:
        image_urls = [image_url]
    else:
        image_urls = None

    # Example processing (this is where the pairing logic would go)
    if pairing_type == "Food Pairing":
        chain = chain_recommend_food()
    else:
        chain = chain_recommend_wine()

    response = chain.invoke(
        {
            "query": description,
            "image_urls": image_urls,
        }
    )
    st.write(response)
