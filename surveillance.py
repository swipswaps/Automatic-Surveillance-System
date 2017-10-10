import numpy as np
import cv2, time, pandas
from datetime import datetime
import getpass
from sendemail import send_email

def start_surveillance(sender,receives,password):

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    
    #Initializations for graph
    status_list=[None,None]
    times=[]
    df=pandas.DataFrame(columns=["Start","End"])

    # Initializations for saving the video!
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output.mp4',fourcc, 15.0, (640,480))
    cap = cv2.VideoCapture()
    cap.open(0)
    counter = 0
    
    while 1:
        status=0
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in face:
            status=1
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),1)
            out.write(img)

        status_list.append(status)
        status_list=status_list[-2:]

        if status_list[-1]==1 and status_list[-2]==0:
            times.append(datetime.now())
        if status_list[-1]==0 and status_list[-2]==1:
            times.append(datetime.now())

        cv2.imshow('img',img)
        k = cv2.waitKey(1)
        if k==ord('q'):
            if status==1:
                times.append(datetime.now())
            break
        
    for i in range(0,len(times),2):
        df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
    df.to_csv("Times.csv")
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    send_email(sender,password,receivers,'First Alert')


if __name__ == '__main__':
    sender = 'automaticsurveillance@gmail.com'
    #receivers=input('Enter the Receiver Email_address: ')
    receivers = ['sahil8sharma8@gmail.com', 'sneh.rathore96@gmail.com', 'parthbhasin96@gmail.com']
    password = getpass.getpass("Password:")
    start_surveillance(sender,receivers,password)  
    