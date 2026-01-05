import cv2
import pickle
import os
import cvzone
import face_recognition
import numpy as np
from Supabase_client import supabase
from datetime import datetime
def attendance():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
    cam.set(3, 370)  # Set width
    cam.set(4, 280) # Set height
    img_bg = cv2.imread("Resources/background.jpg")

    if not cam.isOpened():
        print("Cannot open camera")
        exit()

    ModePath = "Resources/Modes"
    Modes = os.listdir(ModePath)
    ImgModeList = []
    for Mode in Modes:
        ImgModeList.append(cv2.imread(os.path.join(ModePath, Mode)))
    for i in range(0, len(ImgModeList)):
        ImgModeList[i] = cv2.resize(ImgModeList[i], (238,364))
    # print(len(ImgModeList))
    file = open('Encode.pickle', 'rb')
    EncodedListWithIds = pickle.load(file)
    file.close()
    EncodedList, StudentIds = EncodedListWithIds
    #print(StudentIds)
    modetype = 0
    counter = 0
    Id=-1
    imgStudent = []
    student = {}
    stop = False
    while not stop:
        success, img = cam.read()
        img = cv2.resize(img, (370,280))
        imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
        ImgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurrFrame = face_recognition.face_encodings(imgS,faceCurFrame)


        img_bg[85:85+280, 25:25+370] = img
        img_bg[21:21+364, 457:457+238] = ImgModeList[modetype]
        if faceCurFrame:
            for EncodeFace, FaceLoc in zip(encodeCurrFrame, faceCurFrame):
                matches = face_recognition.compare_faces(EncodedList, EncodeFace)
                Faceids = face_recognition.face_distance(EncodedList, EncodeFace) #least distance is a better match

                matchIndex = np.argmin(Faceids)

                if matches[matchIndex]:
                    y1, x2, y2, x1 = FaceLoc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    bbox = 55+x1, 85+y1, x2-x1, y2-y1
                    img_bg= cvzone.cornerRect(img_bg, bbox,t=1, rt=0)
                    Id = StudentIds[matchIndex]
                    if counter == 0:
                        counter = 1
                        modetype = 1

            if counter != 0:
                if counter == 1:
                    #User Image from the storage
                    bucket = supabase.storage.from_("Images")
                    image_bytes = bucket.download(f"{Id}.jpg")
                    array = np.frombuffer(image_bytes, dtype=np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)

                    #User Data
                    studentInfo = supabase.table("Students") \
                        .select("*") \
                        .eq("id", Id) \
                        .execute()
                    student = studentInfo.data[0]

                    #update attendance
                    last_attendance = student.get("last_attendance")
                    if last_attendance:
                        datetimeobj = datetime.fromisoformat(last_attendance.replace("Z", ""))
                    else:
                        datetimeobj = datetime.min

                    #print(datetimeobj)
                    datetimenow = datetime.now()
                    #print(datetimenow)
                    secElapsed = (datetimenow - datetimeobj).total_seconds()
                    #print(secElapsed)
                    if secElapsed > 86400:  #for one day
                        student["total_attendance"]+=1
                        supabase.table("Students") \
                            .update({
                            "total_attendance": student["total_attendance"],
                            "last_attendance": datetimenow.isoformat()
                        }) \
                            .eq("id", Id) \
                            .execute()

                    else:
                        modetype = 3
                        counter = 0
                        img_bg[21:21+364, 457:457+238] = ImgModeList[modetype]


                if modetype != 3:
                    if 5<counter<10:
                        modetype = 2
                        print("Mode 2")
                    img_bg[21:21+364, 457:457+238] = ImgModeList[modetype]


                    if counter<=5:
                        cv2.putText(img_bg, str(student["total_attendance"]), (488, 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)
                        cv2.putText(img_bg, str(student["id"]), (566,279), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.4, (255,255,255), 1 )
                        cv2.putText(img_bg, str(student["Major"]), (571,312), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.4, (255,255,255), 1 )
                        cv2.putText(img_bg, str(student["standing"]), (516,359), cv2.FONT_HERSHEY_COMPLEX, 0.5, (100,100,100), 1 )
                        cv2.putText(img_bg, str(student["year"]), (582,359), cv2.FONT_HERSHEY_COMPLEX, 0.5, (100,100,100), 1 )
                        cv2.putText(img_bg, str(student["starting_year"]), (636,359), cv2.FONT_HERSHEY_COMPLEX, 0.5, (100,100,100), 1 )
                        (w,h),_ = cv2.getTextSize(str(student["Name"]), cv2.FONT_HERSHEY_COMPLEX, 0.7, 1)
                        offset = (238-w)//2 #to centralize name
                        cv2.putText(img_bg, str(student["Name"]), (455+offset,259), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0),1 )

                        img_bg[96:96+128,512:512+128] = imgStudent

                    counter+=1
                    if counter>=10:
                        counter=0
                        modetype=0
                        student = {}
                        imgStudent=[]
                        img_bg[21:21+364, 457:457+238] = ImgModeList[modetype]
                    print("Counter: ", counter)

        else:
            counter = 0
            modetype = 0


            #cv2.imshow("Webcam", img)
        cv2.imshow("Student Attendance System", img_bg)
        key = cv2.waitKey(5) & 0xFF
        if key == ord('q'):
            break
        if cv2.getWindowProperty("Student Attendance System",cv2.WND_PROP_VISIBLE)<1:
            break
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    attendance()