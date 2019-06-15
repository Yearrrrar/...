#coding=utf-8
import time
import cv2
#初始化 opencv 的 Cascade Classification,它的作用是产生一个检测器
faceCascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")
image = cv2.imread("01.jpg")

#图像灰度化
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#调用
time1=time.time()
faces = faceCascade.detectMultiScale(gray,scaleFactor=1.15,minNeighbors=5,minSize=(5,5))
time2=time.time()
print "Found {0} faces!".format(len(faces))
print '共耗时：'+str(time2-time1)+'s'

#######显示图像并用标记框标出来
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
cv2.imshow("Faces found", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
