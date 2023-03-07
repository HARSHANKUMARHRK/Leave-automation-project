import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
def mail_attendance():
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


