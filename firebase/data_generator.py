import datetime
from collections import Counter
import pandas as pd
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
import json


<<<<<<< HEAD
from ..attendance_dashboard import firebase_config
=======
config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": ",
    "messagingSenderId": ""
>>>>>>> f3665f310856e5aa104a6de898911b73e23ec174

config = firebase_config.get_pyrebase_config()
firebase_config.initialize_firebase_admin()



firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database=firebase.database()

def forgot_password(email):
    auth.send_password_reset_email("manojromina1997@gmail.com")

def get_batch(rollno):
    if rollno < 20:
        return "Batch 1"
    elif rollno >=20 and rollno <= 40:
        return "Batch 2"
    else:
        return "Batch 3"

def generate_teacher_id(branch,tid):
    return "FA_"+branch[:2]+"_"+str(tid)

def generate_student_id(branch,year,rollno):
    return branch[:2]+"_"+year+str(rollno)

def user_faculty_generation():
    ref = db.reference('Users')
    student_df = pd.read_csv('firebase/data/comps_faculty.csv')

    for rows in student_df.iterrows():

        name = rows[1][0]
        email = rows[1][1]
        subject = rows[1][4]
        year = rows[1][3]
        branch = rows[1][2]
        password = rows[1][5]
        photos = rows[1][6]
        tid = rows[1][7]

        # user = auth.create_user_with_email_and_password(email, password)
        user = auth.sign_in_with_email_and_password(email, password)
        uid = user['localId']
        print(uid)
        #
        id = generate_teacher_id(branch,tid)
        #
        # ref.child(uid).set({"id": id, "role": 1})
        # print({"id": id, "role": 2})
        database.child('Faculty').child(id).set({"name": name, "branch": branch, "photos": photos})
        print({"name": name, "branch": branch, "photos": photos})
        db.reference('Map').child("Subjects").child(branch).child(year).child(subject).set({"faculty_id":id})


def user_student_generation():

    student_df = pd.read_csv('firebase/data/comps_student.csv')
    student_df = student_df.iloc[15:30]

    id_list = []
    for rows in student_df.iterrows():
        name = rows[1][0]
        email = rows[1][1]
        rollno = rows[1][3]
        year = rows[1][2]
        branch = rows[1][4]
        password = rows[1][5]
        photos = rows[1][6]

        #user = auth.create_user_with_email_and_password(email, password)
        user = auth.sign_in_with_email_and_password(email, password)
        uid = user['localId']
        print(uid)
        batch = get_batch(int(rollno))
        id = generate_student_id(branch,year,rollno)
        id_list.append(id)

        db.reference('Users').child(uid).set({"id":id,"role":2})
        print({"id":id,"role":2})
        db.reference('Students').child(id).set({"name":name,"branch":branch,"year":year,"batch":batch,"photos":photos})
        print({"name":name,"branch":branch,"year":year,"batch":batch,"photos":photos})
        db.reference('Map').child('Students').child(branch).child(year).set(id_list)


def attendance_generation():
    start_date ='2018-03-1'
    end_date = '2018-04-01'
    d1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    d = d2 - d1
    branch = "Comp"
    year = "BE"
    id_list = db.reference('Map').child('Students').child(branch).child(year).get()
    timetable = db.reference('timetable').child(branch).child(year).get()
    subject_faculty = db.reference('Map').child('Subjects').child(branch).child(year).get()
    print(subject_faculty)

    weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    emotions = ['happy','angry','fear','neutral','sadness','disgust']
    for day in range(0,d.days):
        current_date = d1 + datetime.timedelta(day)
        week_day = current_date.weekday()
        day = weekdays[week_day]

        r = random.randrange(7, 10)
        random.shuffle(id_list)
        present_today = id_list[:r]

        if day!=weekdays[-2] and day!=weekdays[-1]:
            date = datetime.datetime.strftime(current_date, "%Y%m%d")
            for time, subject in timetable[day].items():
                r = random.randrange(5,len(present_today))
                random.shuffle(present_today)

                present_for_subject = present_today[:r]
                present_count = 0
                absent_count = 0
                subject_emotion = []
                for id in id_list:
                    if id in present_for_subject:
                        present_count += 1
                        random.shuffle(emotions)
                        p_emotion = emotions[-1]
                        p_subject = subject
                        print((id, p_emotion, p_subject))
                        db.reference('Attendance').child(branch).child(year).child(date).child(id).child(time).set(
                            {"emotion": p_emotion, "subject": subject})
                        db.reference('Map').child('Student_Present').child(id).child(date).child(subject).set({"emotion": p_emotion})
                        subject_emotion.append(p_emotion)
                    else:
                        absent_count += 1
                        db.reference('Map').child('Student_Absent').child(id).child(date).child(subject).set(
                            {"emotion": "NULL"})

                count_subject_emotions = Counter(subject_emotion)

                if subject in subject_faculty.keys():
                    faculty = subject_faculty[subject]
                    faculty_id = faculty['faculty_id']

                    print(subject_faculty)
                    db.reference('Map').child('Subject_Emotions').child(faculty_id).child(date).child(subject).set(
                        {"present": present_count, "absent": absent_count, "emotions": count_subject_emotions})

                    print(subject_emotion)
                db.reference('Map').child('Attendance').child(date).child(subject).set(
                    {"present": present_count, "absent": absent_count, "emotions": count_subject_emotions})

#
# user_student_generation()
#user_faculty_generation()
#attendance_generation()

id_list = db.reference('Map').child('Students').child("Comp").child("BE").get()
print(id_list)


