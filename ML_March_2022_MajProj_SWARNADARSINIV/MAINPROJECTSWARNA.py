import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


cap=cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
volMin,volMax=volume.GetVolumeRange()[:2]
while True:
    success,img = cap.read()
    imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    lmList=[]
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id,lm in enumerate(handlandmark.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                mpDraw.draw_landmarks(img, handlandmark,mpHands.HAND_CONNECTIONS)
            if lmList !=[]:
                x1,y1=lmList[4][1],lmList[4][2]
                x2,y2=lmList[8][1],lmList[8][2]
                cv2.circle(img,(x1,y1),15,(153,51,255),cv2.FILLED)
                cv2.circle(img,(x2,y2),15,(153,51,255),cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(127,0,255),3)
                z1,z2=(x1+x2)//2,(y1+y2)//2
                length=hypot(x2-x1,y2-y1)
                volRange=volume.GetVolumeRange()
                volMin=volRange[0]
                volMax=volRange[1]
                vol=np.interp(length,[50,300],[volMin,volMax])
                volBar=np.interp(length,[50,300],[400,150])
                volPer=np.interp(length,[50,300],[0,100])
                print(vol,length)
            volume.SetMasterVolumeLevel(vol,None)
            cv2.rectangle(img,(50,150),(85,400),(123,213,122),3)
            cv2.rectangle(img,(50,int(volBar)),(85,400),(0,231,23),cv2.FILLED)
            cv2.putText(img,str(int(volPer)),(40,450),cv2.FONT_HERSHEY_PLAIN,4,(24,255,3),3)
                
                
    cv2.imshow('MediaPipe Hands',img)
    cv2.waitKey(1)