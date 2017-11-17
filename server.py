import time
import numpy as np
import cv2
import transmission


class gesture_recog(object):
    def __init__(self,port,baud,cam,flag):
        self.cam = cv2.VideoCapture(cam)            # Video camera object for recordning the frames
        self.ready = False                          # Flag that can be toggled by pressing 's'. True will enable bot signalling else it will only recognize the gesture.
        self.frame = None                           # Variable that references the captured frames
        self.signalling = None                      # Singalling object that will be initiated if bot is ready.
        if flag:
            self.signalling = transmission.signalling(port,baud)

    def frame_read(self):
        """
        Module for preprocessing the captured frames.
        """
        self.frame = self.cam.read()[1]
        target = self.frame[100:350,150:500]
        gray = cv2.cvtColor(target,cv2.COLOR_RGB2GRAY)
        blur_gray = cv2.GaussianBlur(gray,(17,17),0)
        thresh_frame = cv2.threshold(blur_gray,127,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
        return thresh_frame

    def gesture(self):
        """
        Main function where gestures are recognized and communicated with bot.
        """
        while(1):
            bw_frame = self.frame_read()
            contours,heir = cv2.findContours(bw_frame.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                cnt = max(contours, key= lambda x: cv2.contourArea(x))
                cv2.drawContours(self.frame,cnt,-1,(0,255,0),3)
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,0,255),0)
                hull = cv2.convexHull(cnt, returnPoints=False)
                cv2.drawContours(self.frame,[cnt],-1,(0,0,255),3)
                defects = cv2.convexityDefects(cnt,hull)
                fingers = 0
                index = 0
                for i in range(defects.shape[0]):
                    st,en,fr,dist = defects[i,0]
                    start = tuple(cnt[st][0])
                    end = tuple(cnt[en][0])
                    far = tuple(cnt[fr][0])
                    cv2.circle(self.frame,far,5,[255,0,0],-1)
                    cv2.line(self.frame,far,end,[255,255,0],2)
                    cv2.line(self.frame,start,far,[255,255,0],2)
                    if(dist>10000):
                        fingers+=1
                    elif(dist>5000 and dist<10000):
                        index+=1
                if fingers == 4:
                    if self.ready:
                        self.signalling.send('x')       # STOP signal
                    else:
                        print('5')
                elif fingers == 3:
                    if self.ready:
                        self.signalling.send('s')       # REVERSE signal
                    else:
                        print('4')
                elif fingers == 2:
                    if self.ready:
                        self.signalling.send('w')       # FORWARD signal
                    else:
                        print('3')
                elif fingers == 1:
                    if self.ready:
                        self.signalling.send('d')       # RIGHT signal
                    else:
                        print('2')
                elif index == 1:
                    if self.ready:
                        self.signalling.send('a')       # LEFT signal
                    else:
                        print('1')
                else:
                    if self.ready:
                        self.signalling.send('w')       # FORWARD signal (repeated)
                    else:
                        print('closed')
                cv2.imshow('frame', self.frame)
                cv2.imshow('bw_frame', bw_frame)
                key = cv2.waitKey(1)
                if key == ord('s'):                     # Press 's' key whenever bot is ready. This will toggle ready flag and start signalling bot.
                    self.ready = not self.ready
                if key == ord('q'):                     # Press 'q' key to end the execution of program.
                    break   


if __name__ == '__main__':
    """
    Driver function.
    Argument details-
    1. Port number:- On which transmitter is connected. (COM3 in our case)
    2. Baud:- Speed of communication. (9600 in our case)
    3. Cam:- Camera source. This can be either a string that points to the video file or '0' that indicates the default web-cam. (0 in our case)
    4. Flag:- True indicates Bot is ready. False will skip signalling and allow only gesture recognition.
    """
    obj = gesture_recog('COM3',9600,0,False)
    obj.gesture()
