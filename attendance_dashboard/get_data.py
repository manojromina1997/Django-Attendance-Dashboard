import datetime
from collections import Counter,OrderedDict
import pandas as pd
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import random
import json
from . import firebase_config

config = firebase_config.get_pyrebase_config()
firebase_config.initialize_firebase_admin()


weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
emotions = ['happy', 'angry', 'fear', 'neutral', 'sadness', 'disgust']



def get_average_emotions(emotion_dictonary):
    emotions = {'happy': 0, 'surprise': 0, 'neutral': 0, 'disgust': 0, 'angry': 0, 'sadness': 0, 'fear': 0}
    f = {'happy': 1, 'surprise': 2, 'neutral': 3, 'disgust': 4, 'angry': 5, 'sadness': 6, 'fear': 7}
    e = ['happy', 'surprise', 'neutral', 'disgust', 'angry', 'sadness', 'fear']
    """Itterating through each date and getting the absent and present details"""

    print(emotion_dictonary)
    for key, val in emotion_dictonary.items():
        value = f[key]
        count = emotion_dictonary[key]
        emotions.update({key: count * value})
    print(emotions)
    avg = sum(emotions.values()) / len(e)
    index = int(round(avg, 0))
    print(e[index])
    return e[index]


def get_current_student_detail(id):

    """gettting student details from id"""
    student_detail_table = db.reference('Students').get()

    student_detail = student_detail_table[id]
    name = student_detail['name']
    branch = student_detail['branch']
    year = student_detail['year']
    batch = student_detail['batch']

    """Student attendance"""
    student_present_table = db.reference('Map').child('Student_Present').get()
    student_absent_table = db.reference('Map').child('Student_Absent').get()

    """Getting the dates"""
    attendance_list = db.reference('Map').child('Attendance').get()
    date_list = attendance_list.keys()

    """Student present detail"""
    student_present_detail = student_present_table[id]
    present_date = student_present_detail.keys()

    """Student absent detail"""
    student_absent_detail = student_absent_table[id]
    absent_date = student_absent_detail.keys()

    attendance_detail = attendance_list
    attendance_date = list(attendance_detail.keys())

    present_subject_list = []
    absent_subject_list = []
    present_overall_subject_emotions = []
    present_subject_emotion = {}
    present_count = 0
    absent_count = 0
    total_count = 0

    for date in attendance_date:
        attendance_lecture = list(attendance_detail[date].keys())
        total_count += len(attendance_lecture)


    """Itterating through each date and getting the absent and present details"""
    for date in date_list:
        if date in present_date:
            for i,j in student_present_detail[date].items():
                subject_emotion = []
                present_subject_list.append(i)
                for k in j.values():
                    present_overall_subject_emotions.append(k)

                    """Finding emotions for each subject on different dates"""
                    # if i not in present_subject_emotion.keys():
                    #     subject_emotion.append(k)
                    #     present_subject_emotion.update({i:subject_emotion})
                    # else:
                    #     subject_emotion = present_subject_emotion[i]
                    #     subject_emotion.append(k)
                    #     present_subject_emotion.update({i:subject_emotion})

        else:
            for i,j in student_absent_detail[date].items():
                absent_subject_list.append(i)

    present = OrderedDict(Counter(present_subject_list))
    for sub,count in present.items():
            present_count += count
    absent = OrderedDict(Counter(absent_subject_list))
    for sub,count in absent.items():
            absent_count += count
    present_emotion = Counter(present_overall_subject_emotions)
    # print(present_overall_subject_emotions)
    return name,present,absent,present_count,absent_count,total_count,student_present_detail,present_emotion


def get_faculty_detail(id):

    """gettting student details from id"""
    faculty_detail_table = db.reference('Faculty').get()

    faculty_detail = faculty_detail_table[id]
    name = faculty_detail['name']
    branch = faculty_detail['branch']

    """All Student attendance"""
    subject_emotion_table = db.reference('Map').child('Subject_Emotions').child(id).get()

    subject_date = subject_emotion_table.keys()

    """Getting the dates"""
    attendance_list = db.reference('Map').child('Attendance').get()
    date_list = attendance_list.keys()
    number_of_lectures = len(date_list)
    present_list = []
    subject_pie_emotion = {'happy':0, 'surprise':0, 'neutral':0, 'disgust':0, 'angry':0, 'sadness':0, 'fear':0}
    subject_attendance= {}
    overall_subject_emotion = {}
    f = {'happy':1, 'surprise':2, 'neutral':3, 'disgust':4, 'angry':5, 'sadness':6, 'fear':7}

    """Itterating through each date and getting the absent and present details"""
    for date in date_list:
        if date in subject_date:
            subject_emotion = {}
            for s,v in subject_emotion_table[date].items():
                subject_attendance.update({date:v['present']})
                present_list.append(v['present'])
                """calucla1ting emotions """
                emotions = v['emotions']
            for key,val in emotions.items():
                value = f[key]
                count = emotions[key]
                pie_count = subject_pie_emotion[key]
                subject_emotion.update({key:count * value})
                subject_pie_emotion.update({key:pie_count+count})
            avg = sum(subject_emotion.values())/len(f)
            index = int(round(avg,0))
            overall_subject_emotion.update({date:index})
    average_attendance = int(sum(present_list)/len(present_list))
    return subject_attendance,average_attendance,number_of_lectures,overall_subject_emotion,subject_pie_emotion



def get_all_student_data(branch="Comp",year="BE"):
    student_detail_table = db.reference('Students').get()
    student_present_table = db.reference('Map').child('Student_Present').get()
    attendance_table = db.reference('Map').child('Attendance').get()
    students_id_list = db.reference('Map').child('Students').child(branch).child(year).get()
    student_list = []
    for id in students_id_list:
        a = []
        student_detail = student_detail_table[id]
        name = student_detail['name']
        branch = student_detail['branch']
        year = student_detail['year']
        batch = student_detail['batch']
        a.append(id)
        a.append(name)
        a.append(branch)
        a.append(year)
        a.append(batch)

        if id in student_present_table.keys():
            student_present_detail = student_present_table[id]
            present_date = list(student_present_detail.keys())

            attendance_detail = attendance_table
            attendance_date = list(attendance_detail.keys())
            present_count = 0
            absent_count = 0
            total_count = 0
            for date in present_date:
                present_lecture = list(student_present_detail[date].keys())
                present_count += len(present_lecture)
            for date in attendance_date:
                attendance_lecture = list(attendance_detail[date].keys())
                total_count += len(attendance_lecture)
            percentage = int((present_count/total_count) * 100)
            a.append(percentage)

            student_list.append(a)
        else:
            a.append(0)
            student_list.append(a)
    return student_list








        # d = get_date_list('2018-03-01','2018-04-01')
        # for day in range(0, d.days):
        #     current_date = d1 + datetime.timedelta(day)
        #     week_day = current_date.weekday()
        #     day = weekdays[week_day]




# get_current_student_detail('Co_BE5')
# get_faculty_detail('FA_Co_3')
# get_all_student_data('Comp','BE')
