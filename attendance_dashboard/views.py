from django.shortcuts import render,render_to_response
from django.contrib import auth as django_auth
from django.template.context import RequestContext
import pyrebase
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from . import get_data
from . import format_data
import json
from . import firebase_config

config = firebase_config.get_pyrebase_config()



firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database=firebase.database()

def get_users_page(request,role,id):
    print(role)
    print(type(role))
    student_data = db.reference('Map').child('Student_Present').child(id).get()
    teacher_data = db.reference('Map').child('Subject_Emotions').child(id).get()
    attendance_data = db.reference('Map').child('Attendance').get()

    if role == 2 and student_data is not None:
        print("Student")

        student = get_student_data(id)
        print(student)
        return render(request, "student_index.html",student)

    elif role == 1 and teacher_data is not None:
        print("Faculty")
        faculty = get_faculty_data(id)
        print(faculty)
        return render(request, "faculty_index.html",faculty)
    elif role == 0 and attendance_data is not None :
        print("Admin")

        # if request.method == "GET":
        #     branch = request.GET.get('branch')
        #     year = request.GET.get('year')
        #     student_detail_table = db.reference('Students').get()
        #     student_present_table = db.reference('Map').child('Student_Present').get()
        #     student_present_table = db.reference('Map').child('Student_Absent').get()
        #     students_id_list = db.reference('Map').child('Students').child(branch).child(year).get()
        #     for student in students_id_list:
        #         print(student_detail_table[student])
        return render(request, "admin_index.html")
    else:
        a = { "total_count": 0,
             "present_count": 0, "absent_count": 0, "present_percent": 0,
             "present": 0, "absent": 0}

        return render(request,"student_index.html",a)


def get_student_data(id):
    name,present, absent, present_count, absent_count,total_count, student_present_detail, present_emotion = get_data.get_current_student_detail(id)
    print(total_count)
    print(present_count)
    present_percentage = int((present_count / total_count) * 100)

    attendance_column_chart = format_data.column_chart(present, absent)
    attendance_pie_chart = format_data.pie_chart(present)
    attendance_calendar_chart = format_data.calendar_attendance_chart(student_present_detail)
    emotion_calendat_chart = format_data.calendar_emotion_chart(present_emotion)
    emotion_donut_chart = format_data.donut_chart(present_emotion)

    a = {"name":name,"subject_emotion":json.dumps(emotion_donut_chart),"attendance_calendar_chart":json.dumps(attendance_calendar_chart),"attendance_column":json.dumps(attendance_column_chart),"attendance_pie":json.dumps(attendance_pie_chart),"total_count":total_count,"present_count":present_count,"absent_count":absent_count,"present_percent":present_percentage,"present":present,"absent":absent}
    return a

def get_faculty_data(id):
    subject_attendance, average_attendance, number_lectures, overall_subject_emotion, subject_pie_emotion = get_data.get_faculty_detail(id)
    subject_pie_emotion_chart = format_data.pie_emotion_chart(subject_pie_emotion)
    subject_attendance_calendar_chart = format_data.calendar_subject_attendance(subject_attendance)
    overall_subject_emotion_calendar = format_data.calendar_emotion_chart(overall_subject_emotion)
    a = {"subject_pie_emotion":json.dumps(subject_pie_emotion_chart),"overall_subject_emotion":json.dumps(overall_subject_emotion_calendar),"subject_attendance":json.dumps(subject_attendance_calendar_chart),'average_attendance':average_attendance,"number_lectures":number_lectures}
    return a


def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

# def home(request):
#     return render(request,"index.html")1

def students(request):
    student_list = get_data.get_all_student_data('Comp', 'BE')
    branch = "Comp"
    year = "BE"

    # if request.method == 'GET':
    #     branch = request.GET.get('branch')
    #     year = request.GET.get('year')
    #     student_list = get_data.get_all_student_data(branch,year)

    query = request.GET.get("q")

    if query:
        if query[:2]!="FA":
            student_detail = get_student_data(query)
            return render(request, "student_index.html", student_detail)
        else:
            faculty_detail = get_faculty_data(query)
            return render(request, "faculty_index.html",faculty_detail)



    return render(request,"students_table.html",{"students":student_list})

def logout(request):
    django_auth.logout(request)
    return render(request, 'login.html')

def dashboard(request):
    # query = request.GET.get("id")
    print(auth.current_user)

    return render(request, 'student_index.html')




def home(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    # Log the user in
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("Inside")
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        users = db.reference('Users').get()
        uid = user['localId']
        role = users[uid]
        print(role)
        page = get_users_page(request, role['role'],role['id'])
        return page

    except:
        message = "Invalid Credential"
        return render(request, "login.html", {"msg": message})
        # return render(request,"login.html")




def forgot_password():
    print("Hi")

def generate_student_id(branch,year,rollno):
    return branch[:2]+"_"+year+str(rollno)

def get_batch(rollno):
    if rollno < 20:
        return "Batch 1"
    elif rollno >=20 and rollno <= 40:
        return "Batch 2"
    else:
        return "Batch 3"
def post_register(request):

    name=request.POST.get('name')
    branch = request.POST.get('branch')
    year = request.POST.get('year')
    rollno = request.POST.get('rollno')
    email=request.POST.get('email')
    password=request.POST.get('password')
    photos = "None"

    try:
        user=auth.create_user_with_email_and_password(email,password)
        uid = user['localId']
        id = generate_student_id(branch, year, rollno)
        batch = get_batch(int(rollno))
        """Getting the previous id of student from same class"""
        id_list = db.reference('Map').child('Students').child(branch).child(year).get()
        id = generate_student_id(branch, year, rollno)
        if id_list is None:
            id_list = []
            id_list.append(id)
        else:
            id_list.append(id)
        db.reference('Users').child(uid).set({"id": id, "role": 2})
        db.reference('Students').child(id).set(
            {"name": name, "branch": branch, "year": year, "batch": batch, "photos": photos})
        db.reference('Map').child('Students').child(branch).child(year).set(id_list)

        return render(request, "login.html")
    except:
        message="Unable to create account try again"
        return render(request,"register.html",{"messg":message})
