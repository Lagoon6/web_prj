from django.shortcuts import render

import requests
import pymysql as m
from datetime import datetime
import json

def mainPage(request):
    current_time = datetime.now()


    con = m.connect(host="localhost",
                user = "root", passwd= "dxa132",
                db = "dashproject1", charset= "utf8")
    cur = con.cursor()
    cur.execute("select contact,attend,morningstart from morning ")
    res = cur.fetchall()
    print(res)
    cur.execute("select name, morningstart from morning ")
    res2 = cur.fetchall()
    cur.execute("select name,attedance from attend order by attedance DESC limit 3 ")
    res3 = cur.fetchall()
    con.close()
    attendance = {}
    for i in range(len(res)):
        if res2[i][1] == None:
            continue
        else:
            diff = current_time-res2[i][1]
            ratio =round(100*(diff.hour*60 + diff.minute)/540,1) #hj ratio 자동 계산은 조원들에게 숙제
            attendance[res2[i][0]] = {"ratio": ratio, "times":diff.strftime("%H:%M"), "img_filename": 
                "images/"+res2[i][0]+".png"} 
    attend_cnt =0
    late_attend_cnt = 0
    early_leave_cnt = 0
    untact_cnt = 0
    absent_cnt = 0
    for i in range(len(res)):
        if res[i][0] == '비대면':
            untact_cnt +=1
            attend_cnt +=1
        else:
            if res[i][1] == '출석':
                attend_cnt +=1;
            elif res[i][1] == '지각':
                late_attend_cnt +=1;
            elif res[i][1] == '조퇴':
                early_leave_cnt +=1;
            else:
                absent_cnt +=1;

    all_list = {}
    all_list["pie_list_data"] = [attend_cnt,late_attend_cnt,untact_cnt,absent_cnt]
    all_list["time"] = current_time
    all_list["attendance_time"] = attendance
    all_list["attendance_best"] = res3 #res3 #hj res은 db에 전부 0 이던데...

    return render(request, 
    'mainPage/my_prj_test_1.html',
    {'data_list':all_list}
  )