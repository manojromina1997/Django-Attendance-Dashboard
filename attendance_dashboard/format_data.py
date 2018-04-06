import re
def column_chart(present,absent):

    a = []

    a.append(['Subject', 'Attendance','Absent'])
    for (s1,p),(s2,abs) in zip(present.items(),absent.items()):
        a.append([s1,p,abs])
    # print(a)
    # print(present)
    # print(absent)
    return a

def pie_chart(present):
    a = []
    a.append(['Subject', 'Attendance'])
    for p,q in present.items():
        a.append([p,q])
    return a

def pie_emotion_chart(present):
    a = []
    a.append(['Subject', 'Emotion'])
    for p,q in present.items():
        a.append([p,q])
    return a


def calendar_attendance_chart(present_detail):
    a = []

    # print(present_detail)
    for d,k in present_detail.items():

        # print(d)
        b = []
        for s,e in k.items():
            b.append(s)
        a.append([(d[:4],d[4:6],d[6:8]),len(b)])


    return a

def calendar_subject_attendance(present_detail):
    a = []

    # print(present_detail)
    for d,k in present_detail.items():
        a.append([(d[:4],d[4:6],d[6:8]),k])


    return a


def calendar_emotion_chart(present_emotion):
    a = []
    #
    # print(present_emotion)
    for d,k in present_emotion.items():
        a.append([(d[:4],d[4:6],d[6:8]),k])
    return a


def donut_chart(present_emotion):
    a = []
    a.append(['Subject', 'Emotions'])
    for s,e in present_emotion.items():
        a.append([s,e])
    return a
