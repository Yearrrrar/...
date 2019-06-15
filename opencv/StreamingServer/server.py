# encoding: utf-8

import io
import time
import picamera
import logging
import SocketServer
from threading import Condition
import threading
import BaseHTTPServer as server
import os

import face_detect
from CreatHtml import CreateHtmlClass

FRAMERATE = 32

PAGE="""\
<html>
<head>
<title>picamera MJPEG streaming demo</title>
</head>
<body>
<h1>PiCamera MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
<div><a href="/save">download mjpeg file</a></div>
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
        self.frame_count = 0
        self.file_num = 0
        self.file_flag = False

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            with self.condition:
                self.frame = buf
                self.condition.notify_all()
                self.frame_count = (self.frame_count + 1) % (6 * FRAMERATE)
                if self.frame_count % (3*FRAMERATE) == 0:
                    aThread = ImageParser(self.frame_count, self.frame, self.frame_count)
                    aThread.start()
                if self.frame_count == 0:
                    if self.file_flag:
                        print self.file_num
                        writeThread = SaveFile(self.buffer.getvalue(), self.file_num)
                        writeThread.start()
                        self.file_num += 1
                        self.file_flag = False
                    self.buffer.truncate()
                    self.buffer.seek(0)
        return self.buffer.write(buf)

class MjpegFileStream(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.condition = Condition()
        self.frame = None
        self.path = path
        # print 'path:', path
    
    def run(self):
        file = open(self.path, 'rb')
        content = file.read()
        file.close()
        frames = content.split(b'\xff\xd8')
        print 'frame num: ', len(frames)
        for iframe in frames:
            self.frame = b'\xff\xd8' + iframe
            self.condition.notify_all()
            time.sleep(1)

class SaveFile(threading.Thread):
     """save file"""
     def __init__(self, content, file_num):
         threading.Thread.__init__(self)
         self.content = content
         self.file = open('save/split'+str(file_num)+'.mjpg', 'wb')
         
     def run(self):
         self.file.write(self.content)
         self.file.close()

class ImageParser(threading.Thread):
     """检测人脸"""
     def __init__(self, threadID, frame, counter):
         threading.Thread.__init__(self)
         self.threadID = threadID
         self.frame = frame
         self.counter = counter
         
     def run(self):
         find = face_detect.detect(self.frame, '.jpg')
         print find
         if find>0: output.file_flag = True

ct_obj = CreateHtmlClass()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            fileStream = MjpegFileStream(self.path[1:])
            fileStream.start()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            print self.path
            err_code,content_type,content = ct_obj.root_html(self.path)
            self.send_response(err_code)
            self.send_header("Content-type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

class StreamingServer(SocketServer.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=FRAMERATE) as camera:
    time.sleep(2)
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
        
