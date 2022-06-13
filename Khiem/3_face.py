import cv2
import numpy as np
from PIL import Image
import pickle
import pyodbc

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);
rec=cv2.face.LBPHFaceRecognizer_create();
rec.read("trainer\\trainningData.yml")
id=0
#thiết lập font chữ
#fontface = cv2.FONT_HERSHEY_SIMPLEX
fontface = cv2.FONT_ITALIC
fontscale = 1
fontcolor = (0,100,0)

#lấy dữ liệu ở db qua ID
def getProfile(id):
    conn = pyodbc.connect("Driver={SQL Server};"
                      "Server=JIN\MSSQLSERVER01;"
                      "Database=DL_AI;"
                      "UID=sa;"
                      "PWD=Jin12122000;"
                      "Trusted_Connection=yes;")
    
    cmd="SELECT * FROM People WHERE ID="+str(id) 
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

while(True):
    #đọc camera
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5)#phát hiện mặt trong ảnh
    for(x,y,w,h) in faces:
        #hiện thị thông tin khuôn mặt nhận dạng được
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getProfile(id)
        if(profile!=None):
            cv2.putText(img, "Name: " + str(profile[1]), (x,y+h+30), fontface, fontscale, fontcolor ,2)
            cv2.putText(img, "Tuoi: " + str(profile[2]), (x,y+h+60), fontface, fontscale, fontcolor ,2)
            cv2.putText(img, "Gioi_tinh: " + str(profile[3]), (x,y+h+90), fontface, fontscale, fontcolor ,2)
        #else:
            #cv2.PutText(cv2.fromarray(img),str(id),(x+y+h),fontface,(0,0,255),2);   
        cv2.imshow('Face',img) 
    if cv2.waitKey(1)==ord('q'):
        break;
cam.release()
cv2.destroyAllWindows()