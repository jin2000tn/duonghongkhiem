import cv2
import mysql.connector
import pyodbc
cam = cv2.VideoCapture(0)#sử dụng camera
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')#sử dụng thư viện nhận diện có sẵn opencv

#hàm thêm mới và cập nhật dữ liệu được lưu trong mysql
def insertOrUpdate(Id,Name, Tuoi, Gt):
    #kết nối với database
    conn = pyodbc.connect("Driver={SQL Server};"
                      "Server=JIN\MSSQLSERVER01;"
                      "Database=DL_AI;"
                      "UID=sa;"
                      "PWD=Jin12122000;"
                      "Trusted_Connection=yes;")
    
    cmd="SELECT * FROM People WHERE ID="+str(Id) 
    cursor=conn.execute(cmd)
    isRecordExist=0
    #dùng for chạy câu lệnh sql thêm mới dữ liệu
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE People SET Name='"+str(Name)+"' WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO People(Id,Name,Tuoi,GioiTinh) Values("+str(Id)+",'"+str(Name)+"'"+","+str(Tuoi)+",'"+str(Gt)+"')"
    conn.execute(cmd)
    conn.commit()
    conn.close()

#nhập thông tin dl mới đưa về hàm insertOrUpdate    
id=input('Nhap id: ')
name=input('Nhap name: ')
tuoi=input('Nhap tuoi: ')
gioiTinh=input('Nhap gioi tinh: ')
insertOrUpdate(id,name, tuoi, gioiTinh)
sampleNum=0
while(True):
    #sử dụng vòng lặp phát hiện mặt trong video
    ret, img = cam.read()#đọc camera
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#chuyển ảnh->ảnh xám
    faces = detector.detectMultiScale(gray, 1.3, 5)#phát hiện đối tượng trong ảnh
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)#khoanh vùng đối tượng
        #incrementing sample number 
        sampleNum=sampleNum+1
        #saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User."+id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])#lưu ảnh vào folder
        cv2.imshow('frame',img)#show came
    #wait for 100 miliseconds 
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # dùng lại khi lấy được 21 ảnh
    elif sampleNum>20:
        break
cam.release()