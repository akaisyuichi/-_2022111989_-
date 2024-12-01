from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__, template_folder="travel_html")
app.secret_key = "my_super_secret_key"

import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/main_menu')
def main_menu():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT Name FROM Users WHERE UserID = %s", (user_id,))
    user_name = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    return render_template('main_menu.html', user_name=user_name)



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # 이메일 중복 확인
        connection = connect_to_db()
        try:
            cursor = connection.cursor()
            query_check = "SELECT COUNT(*) FROM Users WHERE Email = %s"
            cursor.execute(query_check, (email,))
            result = cursor.fetchone()

            if result[0] > 0:
                # 이미 존재하는 이메일인 경우
                return render_template("register.html", error="이미 가입된 이메일입니다. 다른 이메일을 사용해주세요.")

        finally:
            cursor.close()
            connection.close()

        # 이메일 중복이 없을 경우 회원가입 진행
        register_user(name, email, password)  # 기존 함수 호출
        return redirect(url_for("register_success"))  # 회원가입 성공 페이지로 리다이렉트
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = login_user(email, password)  # 기존 함수 호출

        if user:
            # 세션에 사용자 정보 저장
            session["user_id"] = user["UserID"]
            session["user_name"] = user["Name"]
            return redirect(url_for("main_menu"))  # 메인 메뉴로 이동
        else:
            return render_template("login_fail.html")  # 로그인 실패 시
    return render_template("login.html")



@app.route("/logout")
def logout():
    session.clear()  # 세션 초기화
    return redirect(url_for("home"))  # 홈 페이지로 이동

    

@app.route("/login_success")
def login_success():
    return render_template("login_success.html")

@app.route("/login_fail")
def login_fail():
    return render_template("login_fail.html")

@app.route("/add_trip", methods=["GET", "POST"])
def add_trip():
    # 로그인 상태 확인
    if "user_id" not in session:
        return redirect(url_for("login"))  # 세션이 없으면 로그인 페이지로 리다이렉트

    error_message = None  # 오류 메시지 초기화

    if request.method == "POST":
        # 여행 계획 추가 로직
        trip_name = request.form["trip_name"]
        destination = request.form["destination"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        # 여행 계획과 겹치는지 확인
        connection = connect_to_db()
        cursor = connection.cursor(dictionary=True)
        query_check_overlap = """
            SELECT COUNT(*) AS overlap_count
            FROM Trips
            WHERE UserID = %s AND NOT (EndDate < %s OR StartDate > %s)
        """
        cursor.execute(query_check_overlap, (session["user_id"], start_date, end_date))
        overlap_count = cursor.fetchone()["overlap_count"]

        if overlap_count > 0:
            error_message = "다른 여행 계획과 날짜가 겹칩니다. 다시 입력해주세요."
        else:
            # 중복이 없는 경우 DB에 저장
            query_insert_trip = """
                INSERT INTO Trips (UserID, TripName, Destination, StartDate, EndDate)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert_trip, (session["user_id"], trip_name, destination, start_date, end_date))
            connection.commit()
            cursor.close()
            connection.close()
            # 성공 시 일정 추가 화면으로 이동
            return redirect(url_for("add_activity", trip_id=cursor.lastrowid))

        cursor.close()
        connection.close()

    # 기존 여행 계획 가져오기
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    query_get_trips = """
        SELECT TripName, Destination, StartDate, EndDate
        FROM Trips
        WHERE UserID = %s
    """
    cursor.execute(query_get_trips, (session["user_id"],))
    trips = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("add_trip.html", trips=trips, error_message=error_message)



@app.route('/save_trip/<int:trip_id>', methods=['POST'])
def save_trip(trip_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 저장 로직이 필요한 경우 처리 후 메인 메뉴로 이동
    return redirect(url_for('main_menu'))



@app.route("/view_trips")
def view_trips():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT TripID, TripName, StartDate, EndDate
        FROM Trips
        WHERE UserID = %s
    """
    cursor.execute(query, (session["user_id"],))
    trips = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("view_trips.html", trips=trips)



@app.route("/view_trip/<int:trip_id>")
def view_trip(trip_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)

    query_trip = """
        SELECT TripName, StartDate, EndDate
        FROM Trips
        WHERE TripID = %s AND UserID = %s
    """
    cursor.execute(query_trip, (trip_id, session["user_id"]))
    trip_info = cursor.fetchone()

    if not trip_info:
        cursor.close()
        connection.close()
        return "해당 여행 계획을 찾을 수 없습니다.", 404

    query_activities = """
        SELECT Name, Type, VisitDate,
               DATE_FORMAT(StartTime, '%H:%i') AS StartTime,
               DATE_FORMAT(EndTime, '%H:%i') AS EndTime
        FROM Activities
        WHERE TripID = %s
        ORDER BY VisitDate, StartTime
    """
    cursor.execute(query_activities, (trip_id,))
    activities = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("view_trip.html", trip_info=trip_info, activities=activities)


@app.route('/modify_trip')
def modify_trip():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)  # 반드시 dictionary=True 설정
    cursor.execute("SELECT TripID, TripName FROM Trips WHERE UserID = %s", (user_id,))
    trips = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('modify_trip.html', trips=trips)

@app.route('/edit_trip_menu/<int:trip_id>')
def edit_trip_menu(trip_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 데이터베이스 연결
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)

    # 여행 계획 이름 가져오기
    query = "SELECT TripName FROM Trips WHERE TripID = %s AND UserID = %s"
    cursor.execute(query, (trip_id, session['user_id']))
    trip = cursor.fetchone()

    cursor.close()
    connection.close()

    if not trip:
        return "해당 여행 계획을 찾을 수 없습니다.", 404

    # 여행 계획 이름과 ID를 템플릿에 전달
    return render_template('edit_trip_menu.html', trip_name=trip['TripName'], trip_id=trip_id)


import os

def load_data_from_txt():
    file_path = "restaurants_and_attractions.txt"
    if not os.path.exists(file_path):
        print("데이터 파일이 존재하지 않습니다. 프로그램을 종료합니다.")
        exit()

    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        next(file)  # 첫 줄(헤더) 건너뛰기
        for line in file:
            name, type_, region = line.strip().split("\t")
            data.append({"Name": name, "Type": type_, "Region": region})
    return data

from datetime import datetime

@app.route('/add_activity/<int:trip_id>', methods=['GET', 'POST'])
def add_activity(trip_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)

    # 여행 계획 기본 정보 가져오기
    query_trip = """
        SELECT TripName, Destination, StartDate, EndDate 
        FROM Trips 
        WHERE TripID = %s AND UserID = %s
    """
    cursor.execute(query_trip, (trip_id, session['user_id']))
    trip_info = cursor.fetchone()

    if not trip_info:
        cursor.close()
        connection.close()
        return "해당 여행 계획을 찾을 수 없습니다.", 404

    error_message = None

    if request.method == 'POST':
        place_name = request.form['place_name']
        visit_date = request.form['visit_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        try:
            query_insert = """
                INSERT INTO Activities (TripID, Name, VisitDate, StartTime, EndTime)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert, (trip_id, place_name, visit_date, start_time, end_time))
            connection.commit()
        except Exception as e:
            # 트리거로부터 반환된 오류 메시지에서 숫자를 제거
            error_message = str(e).split(":")[-1].strip()

            # 현재 추가된 일정 목록 가져오기
            query_activities = """
                SELECT Name, VisitDate, 
                       DATE_FORMAT(StartTime, '%H:%i') AS StartTime, 
                       DATE_FORMAT(EndTime, '%H:%i') AS EndTime 
                FROM Activities 
                WHERE TripID = %s
                ORDER BY VisitDate, StartTime
            """
            cursor.execute(query_activities, (trip_id,))
            activities = cursor.fetchall()

            # 음식점 및 관광지 데이터 가져오기
            query_destination = "SELECT Destination FROM Trips WHERE TripID = %s"
            cursor.execute(query_destination, (trip_id,))
            destination = cursor.fetchone()['Destination']

            places = [place for place in load_data_from_txt() if place[0] == destination]

            cursor.close()
            connection.close()

            return render_template(
                'add_activity.html', 
                trip_id=trip_id, 
                trip_info=trip_info, 
                activities=activities, 
                places=places, 
                error_message=error_message
            )

    # GET 요청 및 추가된 일정 목록 가져오기
    query_activities = """
        SELECT Name, VisitDate, 
               DATE_FORMAT(StartTime, '%H:%i') AS StartTime, 
               DATE_FORMAT(EndTime, '%H:%i') AS EndTime 
        FROM Activities 
        WHERE TripID = %s
        ORDER BY VisitDate, StartTime
    """
    cursor.execute(query_activities, (trip_id,))
    activities = cursor.fetchall()

    # 음식점 및 관광지 데이터 가져오기
    query_destination = "SELECT Destination FROM Trips WHERE TripID = %s"
    cursor.execute(query_destination, (trip_id,))
    destination = cursor.fetchone()['Destination']

    places = [place for place in load_data_from_txt() if place[0] == destination]

    cursor.close()
    connection.close()

    return render_template(
        'add_activity.html', 
        trip_id=trip_id, 
        trip_info=trip_info, 
        activities=activities, 
        places=places, 
        error_message=error_message
    )

@app.route('/save_activity/<int:trip_id>', methods=['POST'])
def save_activity(trip_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 여행 계획 추가 -> 일정 추가의 경우 메인 메뉴로 이동
    if 'from_add_trip' in request.form and request.form['from_add_trip'] == 'true':
        return redirect(url_for('main_menu'))

    # 여행 계획 수정 -> 일정 추가의 경우 뒤로가기 역할
    return redirect(url_for('edit_trip_menu', trip_id=trip_id))


@app.route('/save_and_exit/<int:trip_id>', methods=['POST'])
def save_and_exit(trip_id):
    # 사용자가 저장 버튼을 눌렀을 때 메인 메뉴로 돌아가는 기능
    return redirect(url_for('main_menu'))


@app.route('/modify_activity/<int:trip_id>', methods=['GET', 'POST'])
def modify_activity(trip_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        # POST 요청 처리: 새 시간으로 일정 수정
        activity_id = request.form['activity_id']
        new_start_time = request.form['start_time']
        new_end_time = request.form['end_time']

        # 시간 겹침 확인
        query_overlap = """
            SELECT COUNT(*) AS overlap_count FROM Activities 
            WHERE TripID = %s AND VisitDate = (
                SELECT VisitDate FROM Activities WHERE ActivityID = %s
            ) 
            AND ActivityID != %s 
            AND NOT (EndTime <= %s OR StartTime >= %s)
        """
        cursor.execute(query_overlap, (trip_id, activity_id, activity_id, new_start_time, new_end_time))
        overlap_count = cursor.fetchone()['overlap_count']

        if overlap_count > 0:
            cursor.close()
            connection.close()
            return "일정 시간이 겹칩니다. 다시 입력해주세요.", 400

        # 일정 수정
        query_update = """
            UPDATE Activities 
            SET StartTime = %s, EndTime = %s 
            WHERE ActivityID = %s
        """
        cursor.execute(query_update, (new_start_time, new_end_time, activity_id))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('edit_trip_menu', trip_id=trip_id))

    # GET 요청 처리: 기존 일정 가져오기
    query_activities = """
        SELECT ActivityID, Name, VisitDate, StartTime, EndTime 
        FROM Activities 
        WHERE TripID = %s
        ORDER BY VisitDate, StartTime
    """
    cursor.execute(query_activities, (trip_id,))
    activities = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('modify_activity.html', trip_id=trip_id, activities=activities)

@app.route('/edit_activity/<int:activity_id>', methods=['GET', 'POST'])
def edit_activity(activity_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        # POST 요청: 수정된 일정 정보 저장
        new_start_time = request.form['start_time']
        new_end_time = request.form['end_time']

        # 기존 일정 가져오기
        query_activity = """
            SELECT TripID, VisitDate FROM Activities 
            WHERE ActivityID = %s
        """
        cursor.execute(query_activity, (activity_id,))
        activity = cursor.fetchone()

        if not activity:
            cursor.close()
            connection.close()
            return "해당 일정이 존재하지 않습니다.", 404

        trip_id = activity['TripID']
        visit_date = activity['VisitDate']

        # 시간 겹침 확인
        query_overlap = """
            SELECT COUNT(*) AS overlap_count FROM Activities 
            WHERE TripID = %s AND VisitDate = %s 
            AND ActivityID != %s 
            AND NOT (EndTime <= %s OR StartTime >= %s)
        """
        cursor.execute(query_overlap, (trip_id, visit_date, activity_id, new_start_time, new_end_time))
        overlap_count = cursor.fetchone()['overlap_count']

        if overlap_count > 0:
            cursor.close()
            connection.close()
            return "수정된 시간이 다른 일정과 겹칩니다. 다시 입력해주세요.", 400

        # 일정 수정
        query_update = """
            UPDATE Activities 
            SET StartTime = %s, EndTime = %s 
            WHERE ActivityID = %s
        """
        cursor.execute(query_update, (new_start_time, new_end_time, activity_id))
        connection.commit()

        cursor.close()
        connection.close()
        return redirect(url_for('edit_trip_menu', trip_id=trip_id))

    # GET 요청: 현재 일정 정보 가져오기
    query_activity = """
        SELECT Name, VisitDate, StartTime, EndTime, TripID FROM Activities 
        WHERE ActivityID = %s
    """
    cursor.execute(query_activity, (activity_id,))
    activity = cursor.fetchone()

    cursor.close()
    connection.close()

    if not activity:
        return "해당 일정이 존재하지 않습니다.", 404

    return render_template('edit_activity.html', activity=activity)

@app.route('/delete_trip/<int:trip_id>', methods=['GET', 'POST'])
def delete_trip(trip_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)  # dictionary=True 추가

    try:
        if request.method == 'POST':
            # 삭제 확인 처리
            query_delete_activities = "DELETE FROM Activities WHERE TripID = %s"
            cursor.execute(query_delete_activities, (trip_id,))

            query_delete_trip = "DELETE FROM Trips WHERE TripID = %s AND UserID = %s"
            cursor.execute(query_delete_trip, (trip_id, session['user_id']))

            connection.commit()
            return redirect(url_for('main_menu'))  # 메인 메뉴로 리다이렉트

        # GET 요청: 삭제 확인 페이지 렌더링
        cursor.execute("SELECT TripName FROM Trips WHERE TripID = %s AND UserID = %s", (trip_id, session['user_id']))
        trip = cursor.fetchone()

        if not trip:
            return "해당 여행 계획을 찾을 수 없습니다.", 404

        return render_template('delete_trip.html', trip_name=trip['TripName'], trip_id=trip_id)

    except Exception as e:
        connection.rollback()
        return f"오류 발생: {e}", 500

    finally:
        cursor.close()
        connection.close()




@app.route('/modify_schedule/<int:trip_id>')
def modify_schedule(trip_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT 
            ActivityID, 
            Name, 
            VisitDate, 
            DATE_FORMAT(StartTime, '%H:%i') AS StartTime, 
            DATE_FORMAT(EndTime, '%H:%i') AS EndTime 
        FROM Activities 
        WHERE TripID = %s
    """
    cursor.execute(query, (trip_id,))
    activities = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('modify_schedule.html', trip_id=trip_id, activities=activities)


@app.route('/delete_schedule/<int:trip_id>', methods=['POST'])
def delete_schedule(trip_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 데이터베이스 연결
    connection = connect_to_db()
    cursor = connection.cursor()
    
    # 관련 활동 및 여행 계획 삭제
    try:
        # 먼저 관련된 활동 삭제
        query_delete_activities = "DELETE FROM Activities WHERE TripID = %s"
        cursor.execute(query_delete_activities, (trip_id,))
        
        # 여행 계획 삭제
        query_delete_trip = "DELETE FROM Trips WHERE TripID = %s AND UserID = %s"
        cursor.execute(query_delete_trip, (trip_id, session['user_id']))
        
        connection.commit()
        return redirect(url_for('modify_trip'))  # 수정할 여행 계획 목록으로 돌아가기
    except Exception as e:
        connection.rollback()
        return f"오류 발생: {e}", 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_activity/<int:activity_id>', methods=['POST'])
def delete_activity(activity_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # 해당 일정의 TripID를 가져옴
        query_get_trip_id = "SELECT TripID FROM Activities WHERE ActivityID = %s"
        cursor.execute(query_get_trip_id, (activity_id,))
        activity = cursor.fetchone()

        if not activity:
            return "삭제할 일정이 존재하지 않습니다.", 404

        trip_id = activity['TripID']

        # 해당 일정 삭제
        query_delete_activity = "DELETE FROM Activities WHERE ActivityID = %s"
        cursor.execute(query_delete_activity, (activity_id,))
        connection.commit()

        return redirect(url_for('modify_schedule', trip_id=trip_id))  # 일정 삭제 후 일정 수정 화면으로 이동
    except Exception as e:
        connection.rollback()
        return f"오류 발생: {e}", 500
    finally:
        cursor.close()
        connection.close()

@app.route('/view_logs')
def view_logs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('view_logs.html')

@app.route('/activity_logs')
def activity_logs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT LogID, ActivityID, ChangeType, ChangedAt, ChangedBy
        FROM ActivityLogs
        ORDER BY ChangedAt DESC
    """
    cursor.execute(query)
    logs = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('activity_logs.html', logs=logs)

@app.route('/trip_logs')
def trip_logs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT LogID, TripID, ChangeType, ChangedAt, ChangedBy
        FROM TripLogs
        ORDER BY ChangedAt DESC
    """
    cursor.execute(query)
    logs = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('trip_logs.html', logs=logs)






# Database Connection Function
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="비빌번호 가림",
        database="travelproject"
    )

# Load Data from TXT
def load_data_from_txt():
    file_path = "restaurants_and_attractions.txt"
    if not os.path.exists(file_path):
        print("데이터 파일이 존재하지 않습니다. 프로그램을 종료합니다.")
        exit()

    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        next(file)  # 첫 줄(헤더) 건너뛰기
        for line in file:
            data.append(line.strip().split("\t"))
    return data

# User Registration
def register_user(name, email, password):
    connection = connect_to_db()
    try:
        cursor = connection.cursor()
        hashed_password = generate_password_hash(password) #해시를 사용하여 비밀번호를 암호화하여 안전하게 보관

        # 먼저 이메일 중복 여부 확인
        query_check = "SELECT COUNT(*) FROM Users WHERE Email = %s"
        cursor.execute(query_check, (email,))
        result = cursor.fetchone()

        if result[0] > 0:
            print("이미 가입된 이메일입니다. 다른 이메일을 사용해주세요.")
            return

        # 이메일 중복이 없을 경우 등록 진행
        query = "INSERT INTO Users (Name, Email, Password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, hashed_password))
        connection.commit()
        print("회원가입이 완료되었습니다!")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


# User Login
def login_user(email, password):
    connection = connect_to_db()
    try:
        cursor = connection.cursor()
        query = "SELECT UserID, Name, Password FROM Users WHERE Email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result and check_password_hash(result[2], password):  # Password 확인(해시 사용)
            print("로그인 성공!")
            return {"UserID": result[0], "Name": result[1]}  # UserID와 Name 반환
        else:
            print("이메일 또는 비밀번호가 올바르지 않습니다.")
            return None
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


# Show Regions
def show_regions(data):
    regions = list(set(row[0] for row in data))
    print("\n=== 큰 지역 목록 ===")
    for idx, region in enumerate(regions, start=1):
        print(f"{idx}. {region}")
    return regions

# Show Places by Region
def show_places_by_region(data, region):
    restaurants = [row for row in data if row[0] == region and row[3] != "관광지"]
    attractions = [row for row in data if row[0] == region and row[3] == "관광지"]

    print("\n=== 음식점 리스트 ===")
    for idx, row in enumerate(restaurants, start=1):
        print(f"{idx}. {row[1]} {row[2]} {row[3]} {row[4]}")

    print("\n=== 관광지 리스트 ===")
    for idx, row in enumerate(attractions, start=1):
        print(f"{chr(96 + idx)}. {row[1]} {row[2]}")

    return restaurants, attractions

from datetime import datetime

def add_travel_plan(user_id, data):
    connection = connect_to_db()
    try:
        cursor = connection.cursor()

        # 기존 여행 계획 날짜 표시
        cursor.execute("SELECT TripName, StartDate, EndDate FROM Trips WHERE UserID = %s", (user_id,))
        existing_trips = cursor.fetchall()
        if existing_trips:
            print("\n=== 현재 여행 계획 ===")
            for trip in existing_trips:
                print(f"{trip[0]}: {trip[1]} ~ {trip[2]}")
        else:
            print("\n현재 여행 계획이 없습니다.")

        # 여행 계획 추가
        trip_name = input("\n여행 이름: ")
        start_date_str = input("여행 시작 날짜 (YYYY-MM-DD): ")
        end_date_str = input("여행 종료 날짜 (YYYY-MM-DD): ")

        # 날짜 문자열을 datetime.date 객체로 변환
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # 날짜 겹침 확인
        cursor.execute(
            "SELECT COUNT(*) FROM Trips WHERE UserID = %s AND NOT (EndDate < %s OR StartDate > %s)",
            (user_id, start_date, end_date),
        )
        overlap_count = cursor.fetchone()[0]
        if overlap_count > 0:
            print("오류: 다른 여행 계획과 날짜가 겹칩니다.")
            return

        # 유효한 여행지인지 검증
        valid_destinations = list(set(row[0] for row in data))
        destination = input("여행지: ")
        if destination not in valid_destinations:
            print("오류: 없는 여행지입니다. 여행 계획 추가를 취소합니다.")
            return

        # 여행 계획 삽입
        query = """
            INSERT INTO Trips (UserID, TripName, Destination, StartDate, EndDate)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, trip_name, destination, start_date, end_date))
        trip_id = cursor.lastrowid
        connection.commit()

        print("여행 계획이 추가되었습니다!")

        # 여행지에 따른 음식점과 관광지 필터링
        restaurants = [row for row in data if row[0] == destination and row[3] != "관광지"]
        attractions = [row for row in data if row[0] == destination and row[3] == "관광지"]

        while True:
            choice = input("일정을 추가하시겠습니까? (Y/N): ").lower()
            if choice == 'y':
                add_activity(trip_id, start_date, end_date, restaurants, attractions)
            else:
                break
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def modify_travel_plan(user_id, data):
    trip_id = select_trip(user_id)
    if not trip_id:
        return

    connection = connect_to_db()
    try:
        cursor = connection.cursor()

        # 여행 계획 날짜 및 이름 가져오기
        query_trip = "SELECT TripName, Destination, StartDate, EndDate FROM Trips WHERE TripID = %s"
        cursor.execute(query_trip, (trip_id,))
        trip_details = cursor.fetchone()
        if not trip_details:
            print("해당 여행 계획을 찾을 수 없습니다.")
            return

        trip_name, destination, start_date, end_date = trip_details
        print(f"\n=== 여행 계획: {trip_name} ({start_date} ~ {end_date}) ===")

        # 사용자에게 수정 옵션 제공
        print("1. 일정 추가\n2. 일정 수정\n3. 일정 삭제\n4. 여행 계획 삭제")
        modify_choice = input("선택하세요: ")

        if modify_choice == "1":
            # 일정 추가
            print(f"\n=== 여행 지역: {destination} ===")
            restaurants = [row for row in data if row[0] == destination and row[3] != "관광지"]
            attractions = [row for row in data if row[0] == destination and row[3] == "관광지"]

            if restaurants or attractions:
                add_activity(trip_id, start_date, end_date, restaurants, attractions)
            else:
                print("일정을 추가할 음식점이나 관광지가 없습니다.")

        elif modify_choice == "2":
            # 일정 수정
            query = """
                SELECT ActivityID, Name, VisitDate, StartTime, EndTime
                FROM Activities WHERE TripID = %s
                ORDER BY VisitDate, StartTime
            """
            cursor.execute(query, (trip_id,))
            activities = cursor.fetchall()

            if not activities:
                print("수정할 일정이 없습니다.")
                return

            print("\n=== 현재 일정 ===")
            for idx, activity in enumerate(activities, start=1):
                start_time = str(activity[3])[:-3]
                end_time = str(activity[4])[:-3]
                print(f"{idx}. {activity[1]} ({activity[2]} {start_time}~{end_time})")

            selected_idx = int(input("수정할 일정 번호를 선택하세요: ")) - 1
            selected_activity = activities[selected_idx]

            new_start_time = input(f"새로운 시작 시간 (현재: {str(selected_activity[3])[:-3]}): ")
            new_end_time = input(f"새로운 종료 시간 (현재: {str(selected_activity[4])[:-3]}): ")

            # 시간 겹침 검증
            query_overlap = """
                SELECT COUNT(*) FROM Activities
                WHERE TripID = %s AND VisitDate = %s AND ActivityID != %s
                AND NOT (EndTime <= %s OR StartTime >= %s)
            """
            cursor.execute(query_overlap, (trip_id, selected_activity[2], selected_activity[0], new_start_time, new_end_time))
            overlap_count = cursor.fetchone()[0]
            if overlap_count > 0:
                print("오류: 일정 시간이 겹칩니다.")
                return

            # 일정 수정
            query_update = """
                UPDATE Activities
                SET StartTime = %s, EndTime = %s
                WHERE ActivityID = %s
            """
            cursor.execute(query_update, (new_start_time, new_end_time, selected_activity[0]))
            connection.commit()
            print("일정이 수정되었습니다!")

        elif modify_choice == "3":
            # 일정 삭제
            query = """
                SELECT ActivityID, Name, VisitDate, StartTime, EndTime
                FROM Activities WHERE TripID = %s
                ORDER BY VisitDate, StartTime
            """
            cursor.execute(query, (trip_id,))
            activities = cursor.fetchall()

            if not activities:
                print("삭제할 일정이 없습니다.")
                return

            print("\n=== 현재 일정 ===")
            for idx, activity in enumerate(activities, start=1):
                start_time = str(activity[3])[:-3]
                end_time = str(activity[4])[:-3]
                print(f"{idx}. {activity[1]} ({activity[2]} {start_time}~{end_time})")

            selected_idx = int(input("삭제할 일정 번호를 선택하세요: ")) - 1
            selected_activity = activities[selected_idx]

            query_delete = "DELETE FROM Activities WHERE ActivityID = %s"
            cursor.execute(query_delete, (selected_activity[0],))
            connection.commit()
            print("일정이 삭제되었습니다!")

        elif modify_choice == "4":
            # 여행 계획 삭제
            confirm = input(f"'{trip_name}' 여행 계획을 삭제하시겠습니까? (Y/N): ").lower()
            if confirm == 'y':
                query_delete_activities = "DELETE FROM Activities WHERE TripID = %s"
                query_delete_trip = "DELETE FROM Trips WHERE TripID = %s"
                cursor.execute(query_delete_activities, (trip_id,))
                cursor.execute(query_delete_trip, (trip_id,))
                connection.commit()
                print("여행 계획과 관련된 모든 일정이 삭제되었습니다.")
            else:
                print("여행 계획 삭제가 취소되었습니다.")

        else:
            print("잘못된 입력입니다.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


from datetime import datetime

def add_activity(trip_id, start_date, end_date, restaurants, attractions):
    connection = connect_to_db()
    try:
        cursor = connection.cursor()

        print(f"\n=== 일정 추가 (여행 기간: {start_date} ~ {end_date}) ===")

        # 음식점 리스트 출력
        print("\n=== 음식점 리스트 ===")
        for idx, restaurant in enumerate(restaurants, start=1):
            print(f"{idx}. {restaurant[1]} | {restaurant[2]} | {restaurant[3]} | 평점: {restaurant[4]}")

        # 관광지 리스트 출력
        print("\n=== 관광지 리스트 ===")
        for idx, attraction in enumerate(attractions, start=1):
            print(f"{idx + len(restaurants)}. {attraction[1]} | {attraction[2]}")

        # 선택 입력받기
        total_places = restaurants + attractions
        selected_idx = int(input("추가할 장소 번호를 선택하세요: ")) - 1
        selected_place = total_places[selected_idx]

        # 방문 날짜와 시간 입력받기
        visit_date = input("방문 날짜 (YYYY-MM-DD): ")
        start_time = input("방문 시작 시간 (HH:MM): ")
        end_time = input("방문 종료 시간 (HH:MM): ")

        # 날짜 범위 검증
        visit_date_dt = datetime.strptime(visit_date, "%Y-%m-%d").date()

        if visit_date_dt < start_date or visit_date_dt > end_date:
            print("오류: 일정이 여행 계획 날짜 범위를 벗어납니다.")
            return

        # 시간 겹침 검증
        query_overlap = """
            SELECT COUNT(*) FROM Activities
            WHERE TripID = %s AND VisitDate = %s AND NOT (EndTime <= %s OR StartTime >= %s)
        """
        cursor.execute(query_overlap, (trip_id, visit_date, f"{start_time}:00", f"{end_time}:00"))
        overlap_count = cursor.fetchone()[0]
        if overlap_count > 0:
            print("오류: 일정 시간이 겹칩니다.")
            return

        # 올바른 이름 구성 (음식점 이름 또는 관광지 이름 + 지역)
        full_place_name = f"{selected_place[2]} ({selected_place[1]})"

        # 일정 추가
        query = """
            INSERT INTO Activities (TripID, Name, Type, VisitDate, StartTime, EndTime)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        activity_type = "restaurant" if selected_idx < len(restaurants) else "attraction"
        cursor.execute(query, (
            trip_id,
            full_place_name,
            activity_type,
            visit_date,
            f"{start_time}:00",
            f"{end_time}:00"
        ))
        connection.commit()
        print("일정이 추가되었습니다!")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()




def load_places_for_trip(data, trip_id):
    """
    특정 여행(trip_id)에 대해 음식점과 관광지 데이터를 로드.
    """
    connection = connect_to_db()
    try:
        cursor = connection.cursor()
        
        # 여행의 목적지를 가져옴
        query_trip = "SELECT Destination FROM Trips WHERE TripID = %s"
        cursor.execute(query_trip, (trip_id,))
        trip = cursor.fetchone()
        
        if not trip:
            print("해당 여행을 찾을 수 없습니다.")
            return [], []
        
        destination = trip[0]
        
        # 음식점 및 관광지 필터링
        restaurants = [row for row in data if row[0] == destination and row[3] != "관광지"]
        attractions = [row for row in data if row[0] == destination and row[3] == "관광지"]
        
        return restaurants, attractions
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return [], []
    finally:
        cursor.close()
        connection.close()


# Select Trip
def select_trip(user_id):
    connection = connect_to_db()
    try:
        cursor = connection.cursor()
        query = "SELECT TripID, TripName FROM Trips WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        trips = cursor.fetchall()

        if not trips:
            print("등록된 여행 계획이 없습니다.")
            return None

        print("\n=== 여행 계획 목록 ===")
        for trip in trips:
            print(f"{trip[0]}. {trip[1]}")

        selected_trip_id = int(input("여행 번호를 선택하세요: "))
        return selected_trip_id
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def view_travel_plan(user_id):
    trip_id = select_trip(user_id)
    if not trip_id:
        return

    connection = connect_to_db()
    try:
        cursor = connection.cursor()

        query = """
            SELECT VisitDate, Name, StartTime, EndTime
            FROM Activities
            WHERE TripID = %s
            ORDER BY VisitDate, StartTime
        """
        cursor.execute(query, (trip_id,))
        activities = cursor.fetchall()

        if not activities:
            print("일정이 없습니다.")
            return

        print("\n=== 여행 일정 ===")
        for activity in activities:
            visit_date = activity[0]
            name = activity[1]
            start_time = str(activity[2])[:-3]  # 초 단위 제거
            end_time = str(activity[3])[:-3]    # 초 단위 제거
            print(f"{visit_date} - {name} - {start_time} ~ {end_time}")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()



def is_valid_time(start_time, end_time):
    from datetime import datetime

    # 시간 형식을 파싱
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")

    # 종료 시간이 시작 시간보다 앞서지 않아야 함
    return start < end

# View Logs Function
def view_logs():
    connection = connect_to_db()
    try:
        cursor = connection.cursor()
        print("\n=== 로그 보기 ===")
        print("1. 활동 로그 보기 (Activity Logs)")
        print("2. 여행 계획 로그 보기 (Trip Logs)")
        choice = input("선택하세요: ")

        if choice == "1":
            # Query to fetch activity logs (Generated by the Trigger)
            query = """
                SELECT LogID, ActivityID, ChangeType, ChangedAt, ChangedBy
                FROM activitylogs
                ORDER BY ChangedAt DESC
            """
            cursor.execute(query)
            logs = cursor.fetchall()

            if not logs:
                print("활동 로그가 없습니다.")
            else:
                print("\n=== 활동 로그 ===")
                for log in logs:
                    print(f"LogID: {log[0]}, ActivityID: {log[1]}, ChangeType: {log[2]}, "
                          f"ChangedAt: {log[3]}, ChangedBy: {log[4]}")

        elif choice == "2":
            # Query to fetch trip logs (Generated by the Trigger)
            query = """
                SELECT LogID, TripID, ChangeType, ChangedAt, ChangedBy
                FROM triplogs
                ORDER BY ChangedAt DESC
            """
            cursor.execute(query)
            logs = cursor.fetchall()

            if not logs:
                print("여행 계획 로그가 없습니다.")
            else:
                print("\n=== 여행 계획 로그 ===")
                for log in logs:
                    print(f"LogID: {log[0]}, TripID: {log[1]}, ChangeType: {log[2]}, "
                          f"ChangedAt: {log[3]}, ChangedBy: {log[4]}")

        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


# User Deletion
def delete_user(user_id):
    connection = connect_to_db()
    try:
        cursor = connection.cursor()
        
        # 사용자 확인
        confirm = input("계정을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다. (Y/N): ").lower()
        if confirm != 'y':
            print("계정 삭제가 취소되었습니다.")
            return

        # 계정 삭제 (Trips와 Activities는 ON DELETE CASCADE가 설정되어 있어야 함)
        query_user_delete = "DELETE FROM Users WHERE UserID = %s"
        cursor.execute(query_user_delete, (user_id,))
        connection.commit()
        
        print("계정이 삭제되었습니다. 모든 관련 정보도 삭제되었습니다.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

# Main Function 수정
def main():
    data = load_data_from_txt()
    logged_in_user = None

    print("==== 여행 계획 관리 시스템 ====")
    while True:
        if logged_in_user is None:
            print("\n1. 회원가입\n2. 로그인\n3. 계정 삭제\n4. 종료")
            choice = input("선택하세요: ")

            if choice == "1":
                name = input("이름: ")
                email = input("이메일: ")
                password = input("비밀번호: ")
                register_user(name, email, password)

            elif choice == "2":
                email = input("이메일: ")
                password = input("비밀번호: ")
                user = login_user(email, password)
                if user:
                    logged_in_user = user
                    print(f"환영합니다, {logged_in_user['Name']}님!")  # Name 표시
                else:
                    print("로그인 실패.")

            elif choice == "3":
                email = input("이메일: ")
                password = input("비밀번호: ")
                user = login_user(email, password)
                if user:
                    delete_user(user["UserID"])  # 계정 삭제
                else:
                    print("계정 삭제 실패. 이메일 또는 비밀번호가 잘못되었습니다.")

            elif choice == "4":
                print("시스템을 종료합니다.")
                break

            else:
                print("잘못된 입력입니다. 다시 시도하세요.")
        else:
            print(f"\n{logged_in_user['Name']}님, 무엇을 하시겠습니까?")
            print("1. 여행 계획 추가\n2. 여행 계획 수정\n3. 여행 계획 보기\n4. 로그 보기\n5. 로그아웃")
            choice = input("선택하세요: ")

            if choice == "1":
                add_travel_plan(logged_in_user["UserID"], data)  # UserID 전달
            elif choice == "2":
                modify_travel_plan(logged_in_user["UserID"], data)  # UserID 전달
            elif choice == "3":
                view_travel_plan(logged_in_user["UserID"])  # UserID 전달
            elif choice == "4":
                view_logs()  # 로그 보기 추가
            elif choice == "5":
                print("로그아웃되었습니다.")
                logged_in_user = None
            else:
                print("잘못된 입력입니다. 다시 시도하세요.")



if __name__ == "__main__":
    app.run(debug=True)
