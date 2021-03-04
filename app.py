from flask import Flask, render_template, request, redirect
import pymysql
import time
app = Flask(__name__)

@app.route('/test')
def home():
    return '''
    <h1>이건 h1 제목</h1>
    <p>이건 p 본문 </p>
    <a href="https://flask.palletsprojects.com">Flask 홈페이지 바로가기</a>
    '''
"""제대로 된 웹 사이트, 즉 애플리케이션이라는 걸 만들고자 한다면 모든 페이지마다 HTML 파일을 각각 작성할 게 아니라 일관된 구조와 기능을 가진 템플릿(template)을 활용해야 한다.
    -> return render_template("index.html") # 해당 문서를 렌더링해서 반환
    + jinja2 ( 변수, 조건문/반복문 이용  ) 

student_data = {
    1: {"name": "슈퍼맨", "score": {"국어": 90, "수학": 65}},
    2: {"name": "배트맨", "score": {"국어": 75, "영어": 80, "수학": 75}}"""

@app.route('/home')
def homess():
    return render_template('home.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student')
def student():
    # 페이지 값 (디폴트값 = 1)
    page = request.args.get("page", 1, type=int)

    db = pymysql.connect(host="localhost", user="codestates", passwd="0000", db="students", charset="utf8")
    cursor = db.cursor()
    # 게시물의 총 개수 세기
    per_page = 5  # 한 페이지당 개수

    #: 전체 페이지 구하기
    cursor.execute("SELECT COUNT(*) from student")
    tot_count = cursor.fetchone()[0]
    total_page = round(tot_count / per_page)

    query = "SELECT * FROM student LIMIT %s OFFSET %s;"
    cursor.execute(query, (per_page, (page-1) * per_page))
    # MySQL의 OFFSET은 0부터 시작
    data_list = cursor.fetchall()
    print(data_list)

    # pagination btn
    # 페이지 블럭을 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_start = (block_size * block_num) + 1
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)

    db.close()
    return render_template("student.html",data_list=data_list,per_page=per_page,page=page,
                           block_start=block_start,block_end=block_end,total_page=total_page,tot_count=tot_count)

@app.route('/stdinsertform')
def stdinsertform():
    return render_template('stdinsertform.html')

@app.route('/stdinsert', methods=['POST', 'GET'])
def stdinsert():
    ## 어떤 http method를 이용해서 전달받았는지를 아는 것이 필요함
    ## 아래에서 보는 바와 같이 어떤 방식으로 넘어왔느냐에 따라서 읽어들이는 방식이 달라짐
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        ## 넘겨받은 stdname
        stdname = request.args.get('stdname')
        ## 넘겨받은 stdgender
        stdgender = request.args.get('stdgender')
        ## 넘겨받은 stdphone
        stdphone = request.args.get('stdphone')
        ## 넘겨받은 stdbirth
        stdbirth = request.args.get('stdbirth')
        ## else 로 하지 않은 것은 POST, GET 이외에 다른 method로 넘어왔을 때를 구분하기 위함
        print(stdname)
        print(stdgender)
        print(stdphone)
        print(stdbirth)

        sql = "INSERT INTO student (std_name,std_gender,std_phone,std_birth,std_register) VALUES (%s,%s,%s,%s,%s)"

        db = pymysql.connect(host="localhost", user="codestates", passwd="0000", db="students", charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql,(stdname, stdgender, stdphone, stdbirth, time.strftime('%y-%m-%d %H:%M:%S')))
        db.commit()
        db.close()

        return redirect('/student')

@app.route("/std_delete/<id>")
def std_delete(id):
    sql = "DELETE FROM student WHERE std_no = "+id
    db = pymysql.connect(host="localhost", user="codestates", passwd="0000", db="students", charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect('/student')

@app.route("/std_update/<id>", methods=["GET", "POST"])
def std_update(id):
    sql = "SELECT * FROM student WHERE std_no = "+id
    db = pymysql.connect(host="localhost", user="codestates", passwd="0000", db="students", charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()

    if request.method == "GET":
        return render_template("stdupdateform.html", data_list=data_list)
    else:
        ## 넘겨받은 stdname
        stdname = request.form.get('stdname')
        ## 넘겨받은 stdgender
        stdgender = request.form.get('stdgender')
        ## 넘겨받은 stdphone
        stdphone = request.form.get('stdphone')
        ## 넘겨받은 stdbirth
        stdbirth = request.form.get('stdbirth')

        sql = "UPDATE student SET std_name=%s,std_gender=%s,std_phone=%s,std_birth=%s WHERE std_no = "+id

        db = pymysql.connect(host="localhost", user="codestates", passwd="0000", db="students", charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql,(stdname, stdgender, stdphone, stdbirth))
        db.commit()
        db.close()

        return redirect('/student')

@app.route('/lecture')
def lecture():
    # 페이지 값 (디폴트값 = 1)
    page = request.args.get("page", 1, type=int)

    db = pymysql.connect(host="localhost", user="codestates", passwd="0000", db="students", charset="utf8")
    cursor = db.cursor()
    # 게시물의 총 개수 세기
    per_page = 5  # 한 페이지당 개수

    #: 전체 페이지 구하기
    cursor.execute("SELECT COUNT(*) FROM lecture")
    tot_count = cursor.fetchone()[0]
    total_page = round(tot_count / per_page)

    query = "SELECT * FROM lecture l JOIN teacher t ON l.lecture_teacher = t.t_id LIMIT %s OFFSET %s;"
    cursor.execute(query, (per_page, (page-1) * per_page))
    # 파이썬이 아닌 다른 언어에서는 page가 1부터 시작해서 (page-1) 해줘야 하지만,       파이썬의 range()는 0부터 시작하기 때문에 따로 -1 처리를 하지 않았다.
    # 직접 실행해보면 알겠지만, MySQL의 OFFSET은 0부터 시작이다.
    data_list = cursor.fetchall()

    # pagination btn
    # 페이지 블럭을 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_start = (block_size * block_num) + 1
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)

    db.close()
    return render_template("lecture.html",data_list=data_list,per_page=per_page,page=page,
                           block_start=block_start,block_end=block_end,total_page=total_page,tot_count=tot_count)

@app.route('/lectureinsertform')
def lectureinsertform():
    db = pymysql.connect(host="localhost", user="codestates", passwd="0000", db="students", charset="utf8")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM teacher")
    data_list = cursor.fetchall()
    db.close()
    return render_template('lectureinsertform.html',data_list=data_list)

@app.route('/lectureinsert', methods=['POST', 'GET'])
def lectureinsert():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        db = pymysql.connect(host="localhost", user="codestates", passwd="0000", db="students", charset="utf8")
        cursor = db.cursor()

        ## 넘겨받은 stdname
        lecture_name = request.args.get('lecture_name')
        ## 넘겨받은 stdgender
        lecture_teacher = request.args.get('lecture_teacher')
        cursor.execute("SELECT t_id from teacher WHERE t_name='"+lecture_teacher+"';")
        lecture_teacher = cursor.fetchone()[0]
        ## else 로 하지 않은 것은 POST, GET 이외에 다른 method로 넘어왔을 때를 구분하기 위함
        print(lecture_name)
        print(lecture_teacher)

        sql = "INSERT INTO lecture (lecture_name,lecture_teacher) VALUES (%s,%s)"

        cursor.execute(sql,(lecture_name, lecture_teacher))
        db.commit()
        db.close()

        return redirect('/lecture')

@app.route("/lecture_delete/<id>")
def lecture_delete(id):
    sql = "DELETE FROM lecture WHERE lecture_id = "+id
    db = pymysql.connect(host="localhost", user="codestates", passwd="0000", db="students", charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect('/lecture')

@app.route("/lecture_update/<id>", methods=["GET", "POST"])
def lecture_update(id):
    sql = "SELECT * FROM lecture WHERE lecture_id = "+id
    db = pymysql.connect(host="localhost", user="codestates", passwd="0000", db="students", charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()
    cursor.execute("SELECT * FROM teacher")
    teacher_list = cursor.fetchall()
    print(teacher_list)

    if request.method == "GET":
        return render_template("lectureupdateform.html", data_list=data_list, teacher_list=teacher_list)
    else:
        ## 넘겨받은 stdname
        lecture_name = request.form.get('lecture_name')
        ## 넘겨받은 stdgender
        lecture_teacher = request.form.get('lecture_teacher')
        print(lecture_teacher)
        cursor.execute("SELECT t_id from teacher WHERE t_name='"+lecture_teacher+"';")
        lecture_teacher = cursor.fetchone()[0]
        print(lecture_teacher)

        sql = "UPDATE lecture SET lecture_name=%s,lecture_teacher=%s WHERE lecture_id = "+id

        db = pymysql.connect(host="localhost", user="codestates", passwd="0000", db="students", charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql,(lecture_name, lecture_teacher))
        db.commit()
        db.close()

        return redirect('/lecture')


"""@app.route("/student/<int:id>")
def student(id):
    return render_template("student.html", template_name=student_data[id]["name"], template_score=student_data[id]["score"])"""

"""@app.route('/user/<user_name>/<int:user_age>') # 동적페이지 라우팅
def user(user_name, user_age):
    return f'Hello, {user_name}({user_age}세)!' # f-string 포맷을 활용해서 문자열에 변수를 넣고 h1 태그를 적용"""

if __name__ == '__main__':
    app.run(debug=True)
"""app.run() 괄호 안에 debug=True라고 명시하면 해당 파일의 코드를 수정할 때마다 Flask가 변경된 것을 인식하고 다시 시작한다. 
    스터디 용도로 코딩을 할 때 내용을 바로 반영해서 결과를 확인하기 편리하다."""