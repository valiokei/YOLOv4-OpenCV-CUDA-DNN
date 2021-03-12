from multiprocessing import Process
import cv2
from dnn_inference import YOLOv4

GStream1 = "filesrc location=/home/valiokei/Librealsense-Gstreamer-Jatson-Side/src/Gstreamer/rtp_decoder1.sdp ! sdpdemux ! rtph264depay ! queue ! avdec_h264 ! decodebin ! videoconvert ! appsink "
GStream2 = "filesrc location=/home/valiokei/Librealsense-Gstreamer-Jatson-Side/src/Gstreamer/rtp_decoder2.sdp ! sdpdemux ! rtph264depay ! queue ! avdec_h264 ! decodebin ! videoconvert ! appsink "

yolo= YOLOv4.__new__(YOLOv4)
yolo.__init__()

if __name__ == '__main__':
    p1= Process(target = yolo.gstreamer(GStream1))
    # p2= Process(target = yolo.gstreamer(GStream1))
    p1.start() 
    # p2.start()

    p1.join()
    # p2.join()
