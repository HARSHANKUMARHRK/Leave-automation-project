from flask import Flask, render_template,Response, request
import cv2
from base64 import encode
from gettext import install
from importlib.resources import path
from pydoc import classname
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import sheet


app = Flask(__name__)

@app.route('/')

def camera():
    path = "pics"
    images =[]
    classnames = []
    mylist = os.listdir(path)
    print(mylist)
    for cl in mylist:
        curimg=cv2.imread(f'{path}/{cl}')
        images.append(curimg)
        classnames.append(os.path.splitext(cl)[0])
    print(classnames)

    #using functions to encode images

    def findencoding(images):
        encodelist=[]
        for img in images:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        return encodelist

    #defining function for attendance
    def markattendance(name):
        with open("attendance.csv","r+")as f:
            mydatalist=f.readlines()
            namelist=[]
            for line in mydatalist:
                entry = line.split(",")
                namelist.append(entry[0])
            if name not in namelist:
                now =datetime.now()
                dtstring =now.strftime("%H:%M:%S")
                f.writelines(f'\n{name},{dtstring}')

                new_id=sheet.create()    
                sheet_data = [[name,dtstring]]
                sheet.sheet_function(sheet_data,new_id)

    #calling the function
    encodelistknown=findencoding(images)            
    print("encoding completed")

    #capturing video through webcam
    #frame = cv2.resize(frame,(224,224),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    cap=cv2.VideoCapture(-1)

    while True:
        success,img=cap.read()
        #here imgs is small size of our webcam image
        imgs = cv2.resize(img,(224,224),None,0.25,0.25)
        imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
        
        facescurframe=face_recognition.face_locations(imgs)
        encodecurframe=face_recognition.face_encodings(imgs,facescurframe)

        #zip used to satisfy multiple conditions

        for encodeface,faceloc in zip(encodecurframe,facescurframe):
            matches=face_recognition.compare_faces(encodelistknown,encodeface)
            facedis=face_recognition.face_distance(encodelistknown,encodeface)
            print(facedis)
            matchindex=np.argmin(facedis)


            if matches[matchindex]:
                name=classnames[matchindex].upper()
                print(name)
                #addding name and box to the image
                y1,x2,y2,x1 = faceloc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markattendance(name)
            
            cv2.imshow("webcam",img)
            cv2.waitKey(1)

@app.route('/student', methods=['GET', 'POST'])
def student_details():
    if request.method == 'POST':
        # Get student details from the form
        name = request.form['name']
        roll_number = request.form['roll_number']
        email = request.form['email']
        department = request.form['department']
        leave_status = request.files['leave_status']

        # Save the leave status file to disk
        leave_status.save(f'leave_status_{roll_number}.pdf')

        # Do something with the student details (e.g. save them to a database)
        return f'Student details: {name}, {roll_number}, {email}, {department}'
    return render_template('student_form.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
