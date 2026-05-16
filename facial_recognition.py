import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image
import mediapipe as mp

# Initialize Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# Create the storage directory if it doesn't exist
SAVE_DIR = "registered_faces"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

st.title("🆔 User Face Registration (Ultra-Light Edition)")
st.write("Enter your username and take a picture to register.")

username = st.text_input("Enter Username:", placeholder="e.g., john_doe").strip()
img_file_buffer = st.camera_input("Take a snapshot for registration")

if img_file_buffer is not None and username != "":
    # Convert webcam buffer to PIL Image, then to OpenCV format (BGR)
    img = Image.open(img_file_buffer)
    image_np = np.array(img)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR) # Mediapipe needs RGB
    
    st.info("Scanning for face...")
    
    # Process the image with Mediapipe
    results = face_detection.process(image_rgb)
    
    if not results.detections:
        st.error("❌ No face detected! Please look clearly at the camera.")
    elif len(results.detections) > 1:
        st.warning("⚠️ Multiple faces detected. Please make sure only one person is in frame.")
    else:
        # Success! Save the photo under the username
        file_path = os.path.join(SAVE_DIR, f"{username}.jpg")
        cv2.imwrite(file_path, image_bgr)
        
        st.success(f"🎉 Success! Face registered for user: **{username}**")
        st.balloons()

elif img_file_buffer is not None and username == "":
    st.error("⚠️ Please enter a username before taking the picture.")
