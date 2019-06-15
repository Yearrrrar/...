# -*- coding: utf-8 -*-
import multiprocessing as mp
import cv2
import os
import time
 
resX = 320
resY = 240
# 这个是显示窗口大小
 
# The face cascade file to be used
# 这个xml文件是opencv里面自带的，官方已经训练好的检测文件
face_cascade=cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
face_color = (192,220,240)   # 框人脸 线条的颜色
strokeWeight = 3      #这个是线条的宽度
t_start = time.time()
fps = 0

# 人脸检测函数
def get_faces( img ):

    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces, img, gray

# 画框函数，
def draw_frame( faces, img, gray):

    global xdeg
    global ydeg
    global fps
    global time_t
 
    for x, y, w, h in faces:
        # 这个  x y w h 是两组坐标 代表的检测到人脸的顶点坐标(x,y)(w,h)
        cv2.rectangle( img, ( x, y ),( x + w, y + h ), face_color, strokeWeight)
        cv2.putText(img, "Face No." + str( len( faces ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )
        face_gray=gray[y:y+h,x:x+w]
    # 计算FPS
    fps = fps + 1
    sfps = fps / (time.time() - t_start)
    cv2.putText(img, "FPS : " + str( int( sfps ) ), ( 10, 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )
 
    cv2.imshow( "Frame", img )
 
if __name__ == '__main__':

    camera = cv2.VideoCapture(0)
    camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,resX)  
    camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,resY) 
 
    pool = mp.Pool( processes=4 )
 
    read, img = camera.read()
    pr1 = pool.apply_async( get_faces, [ img ] )   
    read, img = camera.read()
    pr2 = pool.apply_async( get_faces, [ img ] )  
    read, img = camera.read() 
    pr3 = pool.apply_async( get_faces, [ img ] )   
    read, img = camera.read()
    pr4 = pool.apply_async( get_faces, [ img ] )   
 
    fcount = 1
 
    while (True):
        read, img = camera.read()
 
        if   fcount == 1:
            pr1 = pool.apply_async( get_faces, [ img ] )
            faces, img, gray=pr2.get()
            draw_frame( faces, img, gray )
 
        elif fcount == 2:
            pr2 = pool.apply_async( get_faces, [ img ] )
            faces, img, gray=pr3.get()
            draw_frame( faces, img, gray )
 
        elif fcount == 3:
            pr3 = pool.apply_async( get_faces, [ img ] )
            faces, img, gray=pr4.get()
            draw_frame( faces, img, gray )
 
        elif fcount == 4:
            pr4 = pool.apply_async( get_faces, [ img ] )
            faces, img, gray=pr1.get()
            draw_frame( faces, img, gray )
            fcount = 0
 
        fcount += 1
 
        if cv2.waitKey(1000 // 12) & 0xff == 27:
            break
# 按q退出
    cv2.destroyAllWindows()