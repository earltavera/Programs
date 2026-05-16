import streamlit as st
import os
from PIL import Image

# Create the storage directory if it doesn't exist
SAVE_DIR = "registered_faces"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

st.title("🆔 User Face Registration (Zero-Fail Edition)")
st.write("Enter your username and take a picture to register.")

# 1. Get Username
username = st.text_input("Enter Username:", placeholder="e.g., john_doe").strip()

# 2. Capture Snapshot
img_file_buffer = st.camera_input("Take a snapshot for registration")

if img_file_buffer is not None and username != "":
    try:
        # Open the image using pure Python Image Library (PIL)
        img = Image.open(img_file_buffer)
        
        # Build the exact file path
        file_path = os.path.join(SAVE_DIR, f"{username}.jpg")
        
        # Save the file natively
        img.save(file_path, "JPEG")
        
        st.success(f"🎉 Success! Image saved and registered for user: **{username}**")
        st.balloons()
        
        # Optional: Show confirmation info
        st.info(f"Saved to local directory as: {file_path}")
        
    except Exception as e:
        st.error(f"❌ An error occurred while saving the image: {e}")

elif img_file_buffer is not None and username == "":
    st.error("⚠️ Please enter a username *before* taking the picture.")
