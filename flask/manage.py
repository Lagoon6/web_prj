from flask import Flask, request, render_template, redirect, session, url_for
import pymysql as m
from datetime import datetime
import json
import requests


app = Flask(__name__)
app.secret_key ='super secret key'
app.config['SESSION TYPE']='filesystem'


@app.route("/",methods=["POST","GET"])
def login():
    con = m.connect(host="localhost",
                user = "root", passwd= "",
                db = "dashproject1", charset= "utf8")
    cur = con.cursor()
    cur.execute("select username,password from accounts ")
    res = cur.fetchall()
    con.close()
    user_info = {}
    for i in range(len(res)):
        user_info[res[i][0]] = res[i][1]
    if request.method =='POST':
        name = request.form['username']
        password = request.form['password']
        try:
            if (name in user_info) :
                if user_info[name] == password:
                    session["logged_in"] = True
                    return redirect('main')
                else:
                    return "비밀번호가 틀렸습니다."
            else:
                return "아이디가 없습니다."
        except:
            return "Error"
    else:
        return render_template('my_login.html')
    

@app.route("/main",methods=["POST","GET"])
def piechart():
    current_time = datetime.now()
    con = m.connect(host="localhost",
                user = "root", passwd= "",
                db = "dashproject1", charset= "utf8")
    cur = con.cursor()
    cur.execute("select contact,attend,morningstart from morning ")
    res = cur.fetchall()
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
            ratio =round(100*(diff.hour*60 + diff.minute)/540,1)
            attendance[res2[i][0]] = {"ratio": ratio, "times":diff.strftime("%H:%M")}
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
    colors = ['#b2c831','#c4d468','#f8f8f8', '#151515']
    pie_list={
        "labels": ['출석', '지각', '비대면', '결석'],
        "datasets": [{
            "backgroundColor": colors[0:4],
            "borderWidth": 0,
            "data": [attend_cnt,late_attend_cnt,untact_cnt,absent_cnt] }]
    }
    all_list = {}
    all_list["pie_list"] =pie_list
    all_list["time"] = current_time
    all_list["attendance_time"] = attendance
    all_list["attendance_best"] = res3
    
    return render_template('my_prj_test_1.html',data_list = all_list)


if __name__ == "__main__":
    app.run(host="localhost", port=5000)