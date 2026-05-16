import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image

# Create the storage directory if it doesn't exist
SAVE_DIR = "registered_faces"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

st.title("🆔 User Face Registration (Clean Server Edition)")
st.write("Enter your username and take a picture to register.")

username = st.text_input("Enter Username:", placeholder="e.g., john_doe").strip()
img_file_buffer = st.camera_input("Take a snapshot for registration")

if img_file_buffer is not None and username != "":
    # Convert webcam buffer directly to an image layout
    img = Image.open(img_file_buffer)
    image_np = np.array(img)
    
    # Convert RGB (Streamlit default) to BGR (OpenCV default for saving files)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    
    st.info("Validating snapshot data...")
    
    # Safety Check: Ensure the picture isn't a blank or empty frame
    if image_np.size == 0 or np.mean(image_np) < 5:
        st.error("❌ Invalid image data. Please ensure your camera is uncovered and try again.")
    else:
        # Success! Save the photo safely under the username
        file_path = os.path.join(SAVE_DIR, f"{username}.jpg")
        cv2.imwrite(file_path, image_bgr)
        
        st.success(f"🎉 Success! Face registered for user: **{username}**")
        st.balloons()

elif img_file_buffer is not None and username == "":
    st.error("⚠️ Please enter a username before taking the picture.")
