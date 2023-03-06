import string    
import random 
import pandas as pd
from pymongo import MongoClient


client = MongoClient("mongodb+srv://leaveletter:2022@leave-letter.e1xgs7e.mongodb.net/?retryWrites=true&w=majority")
db = client['user_login']
mycol = db["leave_data"]

S = 10    

#reading data from csv

df = pd.read_csv("data.csv")
roll = df["rollno"]

#appending roll_num with generated password in db

for i in range(len(roll)):
    ran = ''.join(random.choices(string.ascii_lowercase + string.digits, k = S))    
    print(roll[i], str(ran))
    dictionary = {"_id" : roll[i], "password" : str(ran)}
    y = mycol.insert_one(dictionary)



