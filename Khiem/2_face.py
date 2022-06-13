import cv2,os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path='dataSet'

def getImagesAndLabels(path):
    #lấy đường dẫn của tất cả tệp trong thư mục
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        #Convert ảnh và add vào mảng faces cùng với ID đối với bàn toán classfication 
        # ở đây thì Feature là ảnh còn Label chính là id người dùng
        faceImg=Image.open(imagePath).convert('L');
        faceNp=np.array(faceImg,'uint8')
        #tách lấy ID của ảnh
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        #print (ID)
        IDs.append(ID)
        cv2.imshow("traning",faceNp)
        cv2.waitKey(10)
    return IDs, faces

Ids,faces=getImagesAndLabels(path)
#trainning
recognizer.train(faces,np.array(Ids))#mặt phát hiện train
recognizer.save('trainer/trainningData.yml')#lưu file train dữ liệu
cv2.destroyAllWindows()