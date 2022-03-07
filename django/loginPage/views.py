from django.shortcuts import render
from django.http import HttpResponse
import pymysql as m
from mainPage import views


def loginPage(request):
    return render(request, 
        template_name = 'loginPage/loginPage.html',
    )

def get_post(request):
  if request.method == 'POST': 
    print("POST진입")

    name = request.POST.get('username')
    password = request.POST.get('password')

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

    if name in user_info :
        if user_info[name] == password:
            #return render(request, 'mainPage/mainPage',)
            return views.mainPage(request)

        else:
            return HttpResponse("비밀번호가 틀렸습니다.")
    else:
        return HttpResponse("아이디가 없습니다.")


    #return render(request, 'mainPage/testmain.html')#'mainPage/my_prj_test_1.html')