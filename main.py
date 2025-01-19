import streamlit as st
from database import init_db, save_reference_image, get_reference_images
from file_processing import process_excel, process_pdf
from phone_ui import generate_phone_ui
from image_gen import generate_dalle_image
import pandas as pd
from PIL import Image
import io

# Initialize database connection
conn, cursor = init_db()

# Streamlit UI
st.title("SnapSynth - Image Generation Chatbot")

# File upload section
uploaded_excel = st.file_uploader("Upload Excel File", type=["xlsx"])
uploaded_pdf = st.file_uploader("Upload PDF Guidelines", type=["pdf"])
uploaded_image = st.file_uploader("Upload Reference Image (Optional)", type=["jpg", "jpeg", "png"])

df = None  # Initialize the DataFrame

# Process the Excel file if uploaded
if uploaded_excel:
    try:
        # Load and process the Excel file
        df = process_excel(uploaded_excel)
        st.write("### Excel Data Preview")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error processing Excel file: {e}")

# Password input section
password_input = st.text_input("Enter your password", type="password")

# Validate the password
if st.button("Validate Password"):
    if df is not None and not df.empty:
        # Check if password exists in the Excel sheet
        if password_input:
            matched_user = df[df['Password'].str.lower() == password_input.lower()]
            
            if not matched_user.empty:
                user_data = matched_user.iloc[0]  # Get the first matching user
                
                # Display user info
                st.write(f"### User Found: {user_data['account_holder_name']}")
                st.write(f"Location: {user_data['location']}")
                st.write(f"Favorite Color: {user_data['favorite_color']}")
                
                # Generate the prompt for DALL·E using the user data
                prompt = f"Design a modern and user-friendly bank application UI in English language for the user: {user_data['account_holder_name']}."
                prompt += f"Include location: {user_data['location']}, favorite color: {user_data['favorite_color']}. "
                prompt += f"The UI should be simple and professional, focusing on account details and user interaction."
                
                # Generate the UI using DALL·E
                ui_image_url = generate_dalle_image(prompt)
                
                if ui_image_url:
                    st.image(ui_image_url, caption="Generated Bank Application UI")
                else:
                    st.error("Failed to generate image.")
            else:
                st.error("Password not found. Please try again.")
        else:
            st.warning("Please enter your password.")
    else:
        st.info("Please upload the Excel file first or ensure it has data.")

# Display reference images from the database
if st.button("Show Stored Reference Images"):
    images = get_reference_images(cursor)
    if images:
        for name, img_data in images:
            st.write(f"**{name}**")
            image = Image.open(io.BytesIO(img_data))
            st.image(image)
    else:
        st.info("No reference images found.")

# Close database connection safely at the end
if conn:
    conn.close()