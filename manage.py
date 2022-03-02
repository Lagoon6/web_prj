from flask import Flask, request, render_template, redirect, session, url_for
import pymysql as m
from datetime import datetime
import json
import requests

current_time = datetime.now()

app = Flask(__name__)
app.secret_key ='super secret key'
app.config['SESSION TYPE']='filesystem'


@app.route("/",methods=["POST","GET"])
def login():
    con = m.connect(host="localhost",
                user = "root", passwd= "dxa132",
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
                    return redirect(url_for('main'))
                else:
                    return "비밀번호가 틀렸습니다."
            else:
                return "아이디가 없습니다."
        except:
            return "don't login"
    else:
        return render_template('my_login.html')
    
@app.route("/main",methods=["POST","GET"])
def main():
    return render_template('my_prj_test_1.html',time= current_time)

@app.route("/main",methods=["POST","GET"])
def piechart():
    con = m.connect(host="localhost",
                user = "root", passwd= "dxa132",
                db = "dashproject1", charset= "utf8")
    cur = con.cursor()
    cur.execute("select contact,attend,morningstart from morning ")
    res = cur.fetchall()
    con.close()
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
    all_list={
        "labels": ['출석', '지각', '비대면', '결석'],
        "datasets": [{
            "backgroundColor": "colors".slice(0,4),
            "borderWidth": 0,
            "data": [attend_cnt,late_attend_cnt,untact_cnt,absent_cnt] }]
    }
    return render_template('my_prj_test_1.html',data_list = json.dump(all_list))





apikey ="1c98556bab77208b58bc7cf6168ff0bb"
city_list =["Seoul,KR"]
api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
k2C = lambda k: k -273.15

for name in city_list:
    url = api.format(city=name, key=apikey)
    res = requests.get(url)
    data = json.loads(res.text)
    print("** 도시 = ", data["name"])
    print("| 날씨 = ", data["weather"][0]["description"])
    print("| 최저기온 = ", k2C(data["main"]["temp_min"]))
    print("| 최고기온 = ", k2C(data["main"]["temp_max"]))
    print("| 습도 = ", data["main"]["humidity"])
    print("| 기압 = ", data["main"]["pressure"])
    print("| 풍향 = ", data["wind"]["deg"])
    print("| 풍속 = ", data["wind"]["speed"])
    print(" ")


if __name__ == "__main__":
    app.run(host="localhost", port=5000)