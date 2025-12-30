import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# Page Config
st.set_page_config(page_title="RiSa Bio-Lens", page_icon="🌿")

# Sidebar for API Key (Hidden from public view)
with st.sidebar:
    st.header("Authentication")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter Gemini API Key", type="password")

st.title("🌿 RiSa Bio-Lens")
st.write("Upload a photo of nature (plant, insect, animal) to identify it.")

if api_key:
    genai.configure(api_key=api_key)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        if st.button('Identify'):
            with st.spinner('Analyzing...'):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash-001')
                    prompt = "Identify this living organism. Give its common name, scientific name, and 3 fun facts. If dangerous, warn me."
                    response = model.generate_content([prompt, image])
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("System waiting for API Key...")
