import cv2
import face_recognition
import numpy as np
import os
import pickle

from Supabase_client import supabase  # your existing client

BUCKET_NAME = "Images"  # your Supabase bucket name

imgList = []
StudentIds = []

# Fetch files from Supabase bucket
files = supabase.storage.from_(BUCKET_NAME).list()

for file in files:
    file_name = file["name"]

    # Skip non-image files
    if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    # Download image bytes
    image_bytes = supabase.storage.from_(BUCKET_NAME).download(file_name)

    # Convert bytes to OpenCV image
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        continue

    imgList.append(img)
    StudentIds.append(os.path.splitext(file_name)[0])

print(StudentIds)


# ---------------- ENCODING ----------------
def FindEncodings(images):
    encodelist = []
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        encodes = face_recognition.face_encodings(image)
        if encodes:  # safety check
            encodelist.append(encodes[0])
    return encodelist


EncodeList = FindEncodings(imgList)
EncodedListWithIds = [EncodeList, StudentIds]

with open('Encode.pickle', 'wb') as file:
    pickle.dump(EncodedListWithIds, file)
