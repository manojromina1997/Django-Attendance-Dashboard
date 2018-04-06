import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
import json
from ..attendance_dashboard import firebase_config

config = firebase_config.get_pyrebase_config()
firebase_config.initialize_firebase_admin()

# As an admin, the app has access to read and write all data, regradless of Security Rules
# ref = db.reference('Students')
# a = ref.order_by_key().get()
# b = ref.child('Map').get()
# c = b['Comp']['SE']
# student_list = []
# for i in c:
#     student_list.append(ref.child(i).get())
#     student_list.append(ref.child(i).get())
# print(student_list)
ref = db.reference('timetable').get()

data = json.loads(ref)
df = pd.DataFrame(data)
print(df)

# ref  = db.reference("Attendance_Emotion")
# print(ref.child('Comp').get())
# branch = ref.order_by_child()

# for keys,value in a.items():
#     print(keys)
#     print(value)
