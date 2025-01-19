# utils/image_gen.py
import openai
import streamlit as st

api_key = st.secrets["api_keys"]["openai_key"]
openai.api_key = api_key

def generate_dalle_image(prompt):
    """
    This function will use the OpenAI API to generate an image based on the prompt.
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
