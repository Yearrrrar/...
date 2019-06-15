#coding=utf-8
import time
import cv2
#初始化 opencv 的 Cascade Classification,它的作用是产生一个检测器
faceCascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture("01.mp4")  
while(cap.isOpened()):  
    ret , frame = cap.read()  
    #这里必须判断视频是否读取完毕,否则播放到最后一帧的时候出现问题  
    if ret == True:
        #cv2.imshow("frame" , frame)
        # 图像灰度化
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.15,minNeighbors=5,minSize=(5,5))
        #######显示图像并用标记框标出来
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("Faces found", frame)
    else:  
        break   
    if cv2.waitKey(10) & 0xFF == 27:  
        break  
cap.release()  
cv2.destroyAllWindows()


