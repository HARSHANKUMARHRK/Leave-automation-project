from bson import ObjectId
from flask import Flask, render_template,Response, request,session,redirect,url_for,send_file
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
from pymongo import MongoClient
import PyPDF2
import re
import pytesseract
import cv2
import pdf2image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import data


app = Flask(__name__)
app.secret_key = "abc" 
client = MongoClient("mongodb+srv://leaveletter:2022@leave-letter.e1xgs7e.mongodb.net/?retryWrites=true&w=majority")
db = client['user_login']
mycol = db["leave_data"]

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

@app.route('/login', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        name = request.form["roll_no"]
        password = request.form['password']
        pwd = mycol.find({"_id" : name})[0]["password"]
        print(pwd)

        if pwd == password:
            # messages = json.dumps({"name":name})
            session['roll_no'] = name
            session["pwd"] = pwd
            return redirect(url_for('student_details'))
            # return render_template("dashboard.html", name = name)
        else:
            return render_template("Login.html", pwd = "wrong password")

    return render_template("Login.html")

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # messages = request.args['messages']
    roll_no = session['roll_no']
    print(roll_no)
    # print(json.loads(messages))

    if request.method == 'POST':
        pwd = session["pwd"]
        current_pass = request.form["current_pass"]
        new_pass = request.form["new_pass"]
        re_pass = request.form["re_pass"]

        if pwd == current_pass and new_pass == re_pass:
           

            myquery = { "_id": roll_no }
            newvalues = { "$set": { "password": new_pass } }
            mycol.update_one(myquery, newvalues)
            print("password changed")




        elif pwd != current_pass:
            print("current password incorrect")
        
            


    return render_template("dashboard(1).html", name = roll_no)


@app.route('/student', methods=['GET', 'POST'])
def student_details():
    if request.method == 'POST':

        name = request.form['name']
        roll_number = request.form['roll_number']
        email = request.form['email']
        department = request.form['department']
        leave_status = request.files['leave_status']
        date=request.form["date"]
        year=request.form["year"]
        month=request.form["Month"]

        final=date,"-",month,"-",year
     
        leave_status.save(f'leave_status_{roll_number}.pdf')
        pdf_file = PyPDF2.PdfFileReader(open(f"leave_status_{roll_number}.pdf", "rb"))
        text = pdf_file.getPage(0).extractText()

        file_path = os.path.abspath(f'/home/kishore/Leave-automation-project/leave_status_{roll_number}.pdf')
        pdf_file = f'leave_status_{roll_number}.pdf'
        images = pdf2image.convert_from_path(pdf_file)


        text = pytesseract.image_to_string(images[0])

        print(text.split())
        date_1 = r'(\d{4})[-/\.](\d{2})[-/\.](\d{2})'
        date_pattern = r'(\d{1,2})-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d{4})'
# date_pattern = r'(\d{1,2})-"q@"-(\d{4})'

        match = re.search(date_pattern, text)
        match2=re.search(date_1,text)
        if match or match2:
            date_0 = match.group()
            if(match2):
                date_1=match2.group()
            print(f"Extracted date: {date_0}")
        else:
            print("No date found in text")

        if str(date_0)==str(final).strip():
            a="verified"
        else:
            a="not verified"

        with open(file_path, 'rb') as f:
            image_data = f.read()
        document = {'image': image_data}
        mycol.insert_one(document)
        # with open("data.csv","r+")as f:
        #     f.writelines(f'\n{name},{roll_number},{email},{department},{final}')

        body ="hiiii"
        sender = 'cryptrix22@gmail.com'
        password = 'memusfkyojwjspdr'
        receiver = email
        
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = "This is mail"
        message.attach(MIMEText(body, 'plain'))

        qrimage = f'leave_status_{roll_number}.pdf'

        binary_pdf = open(qrimage, 'rb')
        payload = MIMEBase('application', 'octate-stream', Name=qrimage)
        payload.set_payload((binary_pdf).read())
        encoders.encode_base64(payload)

        payload.add_header('Content-Decomposition', 'attachment', filename=qrimage)
        message.attach(payload)
        message.attach(MIMEText(body, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender, password)
        text = message.as_string()
        session.sendmail(sender, receiver, text)
        session.quit()

        return f'Student details: {name}, {roll_number}, {email}, {department},{a}'
    return render_template('student_form.html')
@app.route('/send_mail',methods=['GET','POST'])
def send_attendance():
    if request.method=='POST':
        df1=pd.read_csv("data.csv")
        names=df1["name"]

        df2=pd.read_csv("attendance.csv")
        final_names=df2["name"]
        # print(final_names)
        att_name=[]
        for j in final_names:
            att_name.append(j)

        # print(att_name)
        l=[]
        result=[]
        for i in names:
            if(i not in att_name):
                l.append(i)
                adj_row=df1[df1["name"]==i]
                mail_id=adj_row["mailid"].values[0]
                result.append(mail_id)

        # print(l)

        print(result)

        for each in result:
            body="This mail is regarding the application of leave"
            sender = 'cryptrix22@gmail.com'
            password = 'memusfkyojwjspdr'
            receiver = each
            message = MIMEMultipart()
            message['From'] = sender
            message['To'] = receiver
            message['Subject'] = "Reminder mail to apply leave"
            message.attach(MIMEText(body, 'plain'))
            qrimage = 'leave.pdf'
            binary_pdf = open(qrimage, 'rb')
            payload = MIMEBase('application', 'octate-stream', Name=qrimage)
            payload.set_payload((binary_pdf).read())
            encoders.encode_base64(payload)

            payload.add_header('Content-Decomposition', 'attachment', filename=qrimage)
            message.attach(payload)

            session = smtplib.SMTP('smtp.gmail.com', 587)

            session.starttls()

            session.login(sender, password)

            text = message.as_string()
            session.sendmail(sender, receiver, text)
            session.quit()


        

    return render_template("attendance.html")



@app.route('/pdf/<id>')
def get_image(id):
    document = mycol.find_one({'_id': ObjectId(id)})
    if not document:
        return 'PDF not found', 404

    pdf_data = document.get('pdf')
 
    response = Response(pdf_data, mimetype='application/pdf')
    
    response.headers.set('Content-Disposition', 'inline', filename='document.pdf')
# @app.route('/pdf')
# def display_pdf():
#     return render_template('pdf.html', filename='leave_status_21.pdf')

# @app.route('/pdf_viewer/<filename>')
# def pdf_viewer(filename):
#     path = 'path/to/your/pdf/files/' + filename
#     return send_file(path, as_attachment=False)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)