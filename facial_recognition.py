import streamlit as st
import face_recognition
import os
from PIL import Image
import numpy as np

# Create the storage directory if it doesn't exist
SAVE_DIR = "registered_faces"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

st.title("🆔 User Face Registration")
st.write("Enter your username and take a picture to register your face in the system.")

# 1. Input for Username
username = st.text_input("Enter Username:", placeholder="e.g., john_doe").strip()

# 2. Webcam Input
img_file_buffer = st.camera_input("Take a snapshot for registration")

# 3. Process and Save
if img_file_buffer is not None and username != "":
    # Convert the picture from the webcam into a numpy array
    img = Image.open(img_file_buffer)
    image_array = np.array(img)
    
    st.info("Processing face alignment...")
    
    # Check if a face actually exists in the image before saving
    face_locations = face_recognition.face_locations(image_array)
    
    if len(face_locations) == 0:
        st.error("❌ No face detected! Please look clearly at the camera and try again.")
    elif len(face_locations) > 1:
        st.warning("⚠️ Multiple faces detected. Please ensure only you are in the frame.")
    else:
        # Success: One face detected. Save the image file mapped to the username.
        # We save as a standard JPEG using the username as the filename
        filename = f"{username}.jpg"
        file_path = os.path.join(SAVE_DIR, filename)
        
        # Save the file
        img.save(file_path)
        
        st.success(f"🎉 Success! Face registered for user: **{username}**")
        st.balloons()

elif img_file_buffer is not None and username == "":
    st.error("⚠️ Please enter a username *before* taking the picture.")