import sys
import cv2
import argparse
import random
import time
from multiprocessing import Process

class YOLOv4:

    def __init__(self):
        """ Method called when object of this class is created. """

        self.args = None
        self.net = None
        self.names = None
        self.GStream1 = "filesrc location=/home/valiokei/Librealsense-Gstreamer-Jatson-Side/src/Gstreamer/rtp_decoder1.sdp ! sdpdemux ! rtph264depay ! queue ! avdec_h264 ! decodebin ! videoconvert ! appsink "
        self.GStream2 = "filesrc location=/home/valiokei/Librealsense-Gstreamer-Jatson-Side/src/Gstreamer/rtp_decoder2.sdp ! sdpdemux ! rtph264depay ! queue ! avdec_h264 ! decodebin ! videoconvert ! appsink "

        self.parse_arguments()
        self.initialize_network()
        self.run_inference()

    def parse_arguments(self):
        """ Method to parse arguments using argparser. """

        parser = argparse.ArgumentParser(description='Object Detection using YOLOv4 and OpenCV4')
        parser.add_argument('--image', type=str, default='', help='Path to use images')
        parser.add_argument('--stream', type=str, default='', help='Path to use video stream')
        parser.add_argument('--cfg', type=str, default='models/yolov4.cfg', help='Path to cfg to use')
        parser.add_argument('--weights', type=str, default='models/yolov4.weights', help='Path to weights to use')
        parser.add_argument('--namesfile', type=str, default='models/coco.names', help='Path to names to use')
        parser.add_argument('--input_size', type=int, default=416, help='Input size')
        parser.add_argument('--use_gpu', default=True, action='store_true', help='To use NVIDIA GPU or not')

        self.args = parser.parse_args()

    def initialize_network(self):
        """ Method to initialize and load the model. """

        self.net = cv2.dnn_DetectionModel(self.args.cfg, self.args.weights)
        
        if self.args.use_gpu:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        else:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            
        if not self.args.input_size % 32 == 0:
            print('[Error] Invalid input size! Make sure it is a multiple of 32. Exiting..')
            sys.exit(0)
        self.net.setInputSize(self.args.input_size, self.args.input_size)
        self.net.setInputScale(1.0 / 255)
        self.net.setInputSwapRB(True)
        with open(self.args.namesfile, 'rt') as f:
            self.names = f.read().rstrip('\n').split('\n')

    def image_inf(self):
        """ Method to run inference on image. """

        frame = cv2.imread(self.args.image)

        timer = time.time()
        classes, confidences, boxes = self.net.detect(frame, confThreshold=0.1, nmsThreshold=0.4)
        print('[Info] Time Taken: {}'.format(time.time() - timer), end='\r')
        
        if(not len(classes) == 0):
            for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
                label = '%s: %.2f' % (self.names[classId], confidence)
                left, top, width, height = box
                b = random.randint(0, 255)
                g = random.randint(0, 255)
                r = random.randint(0, 255)
                cv2.rectangle(frame, box, color=(b, g, r), thickness=2)
                cv2.rectangle(frame, (left, top), (left + len(label) * 20, top - 30), (b, g, r), cv2.FILLED)
                cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_COMPLEX, 1, (255 - b, 255 - g, 255 - r), 1, cv2.LINE_AA)

        cv2.imwrite('result.jpg', frame)
        cv2.imshow('Inference', frame)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            return

    def stream_inf(self):
        """ Method to run inference on a stream. """

        if self.args.stream == 'webcam':
            stream = 0
        elif self.args.stream == 'GStream1':
            stream = self.GStream1
        elif self.args.stream == 'GStream2':
            stream = self.GStream2
        else:
            stream = self.args.stream
            


        source = cv2.VideoCapture(stream)

        b = random.randint(0, 255)
        g = random.randint(0, 255)
        r = random.randint(0, 255)

        while(source.isOpened()):
            ret, frame = source.read()
            if ret:
                timer = time.time()
                classes, confidences, boxes = self.net.detect(frame, confThreshold=0.1, nmsThreshold=0.4)
                print('[Info] Time Taken: {} | FPS: {}'.format(time.time() - timer, 1/(time.time() - timer)), end='\r')
                
                if(not len(classes) == 0):
                    for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
                        label = '%s: %.2f' % (self.names[classId], confidence)
                        left, top, width, height = box

                        cv2.rectangle(frame, box, color=(255, 0, 0), thickness=2)
                        cv2.rectangle(frame, (left, top), (left + len(label) * 20, top - 30), (b, g, r), cv2.FILLED)
                        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

                cv2.imshow('Inference', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    def gstreamer(self,source):
        """ Method to run inference on a stream. """

        source = cv2.VideoCapture(source)

        b = random.randint(0, 255)
        g = random.randint(0, 255)
        r = random.randint(0, 255)

        while(source.isOpened()):
            ret, frame = source.read()
            if ret:
                timer = time.time()
                classes, confidences, boxes = self.net.detect(frame, confThreshold=0.1, nmsThreshold=0.4)
                print('[Info] Time Taken: {} | FPS: {}'.format(time.time() - timer, 1/(time.time() - timer)), end='\r')
                
                if(not len(classes) == 0):
                    for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
                        label = '%s: %.2f' % (self.names[classId], confidence)
                        left, top, width, height = box

                        cv2.rectangle(frame, box, color=(255, 0, 0), thickness=2)
                        cv2.rectangle(frame, (left, top), (left + len(label) * 20, top - 30), (b, g, r), cv2.FILLED)
                        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

                cv2.imshow('Inference', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


    def run_inference(self):

        # if self.args.image == '' and self.args.stream == '':
        #     print('[Error] Please provide a valid path for --image or --stream.')
        #     sys.exit(0)

        if not self.args.image == '':
            self.image_inf()

        elif not self.args.stream == '':
            self.stream_inf()

        cv2.destroyAllWindows()



if __name__== '__main__':
 
    yolo = YOLOv4.__new__(YOLOv4)
    yolo.__init__()
