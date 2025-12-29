import cv2
import face_recognition
import os
import pickle

FolderPath = "Images"
PathList = os.listdir(FolderPath)
imgList = []
StudentIds = []
for Path in PathList:
    img = cv2.imread(os.path.join(FolderPath, Path))
    imgList.append(img)
    StudentIds.append(os.path.splitext(Path)[0])

print(StudentIds)

def FindEncodings(images):
    encodelist = []
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        #image = cv2.resize(image, (128, 128))
        encodelist.append(encode)
    return encodelist

EncodeList = FindEncodings(imgList)
EncodedListWithIds = [EncodeList, StudentIds]
#print(EncodeList)

file = open('Encode.pickle', 'wb')
pickle.dump(EncodedListWithIds, file)
file.close()

