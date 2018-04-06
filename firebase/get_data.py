import datetime
from collections import Counter
import pandas as pd
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
import json

from ..attendance_dashboard import firebase_config
config = firebase_config.get_pyrebase_config()
firebase_config.initialize_firebase_admin()


weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
emotions = ['happy', 'angry', 'fear', 'neutral', 'sadness', 'disgust']

# def get_date_list(start_date,end_date):
#     d1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
#     d2 = datetime.datetime.strptime(end_date, "%Y-%m-%d")
#     d = d2 - d1
#     for
#     return d


def get_current_student_details(id):
    student_detail_table = db.reference('Students').get()

    student_detail = student_detail_table[id]
    name = student_detail['name']
    branch = student_detail['branch']
    year = student_detail['year']
    batch = student_detail['batch']

    student_present_table = db.reference('Map').child('Student_Present').get()
    student_absent_table = db.reference('Map').child('Student_Absent').get()
    students_id_list = db.reference('Map').child('Students').child(branch).child(year).get()



    student_present_detail = student_present_table[id]
    present_date = student_present_detail.keys()
    for date in present_date:
        print(student_present_detail[date])




get_current_student_details('Co_BE5')
