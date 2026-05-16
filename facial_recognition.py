import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image
from deepface import DeepFace

# Create the storage directory if it doesn't exist
SAVE_DIR = "registered_faces"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

st.title("🆔 User Face Registration (Fast Cloud Edition)")
st.write("Enter your username and take a picture to register.")

username = st.text_input("Enter Username:", placeholder="e.g., john_doe").strip()
img_file_buffer = st.camera_input("Take a snapshot for registration")

if img_file_buffer is not None and username != "":
    # Convert webcam buffer to PIL Image, then to OpenCV format (BGR)
    img = Image.open(img_file_buffer)
    image_np = np.array(img)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    
    st.info("Analyzing image for faces...")
    
    try:
        # DeepFace checks if a face exists in the image
        # detector_backend='opencv' is incredibly fast and lightweight
        face_objs = DeepFace.extract_faces(img_path=image_bgr, detector_backend='opencv', enforce_detection=True)
        
        if len(face_objs) == 0:
            st.error("❌ No face detected! Please look clearly at the camera.")
        elif len(face_objs) > 1:
            st.warning("⚠️ Multiple faces detected. Please make sure only one person is in frame.")
        else:
            # Success! Save the photo under the username
            file_path = os.path.join(SAVE_DIR, f"{username}.jpg")
            cv2.imwrite(file_path, image_bgr)
            
            st.success(f"🎉 Success! Face registered for user: **{username}**")
            st.balloons()
            
    except Exception as e:
        # DeepFace throws an error if 'enforce_detection' finds 0 faces
        st.error("❌ Face detection failed. Please center your face in the camera and try again.")

elif img_file_buffer is not None and username == "":
    st.error("⚠️ Please enter a username before taking the picture.")
