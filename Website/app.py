# from flask import Flask, render_template, request, session, url_for, redirect
# import pymysql.cursors
# from util import *
from flask import Flask, render_template, flash, request, url_for, redirect, session, g
from util import *
from hashlib import md5
from random import *
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta



app = Flask(__name__)
app.secret_key = '2y14ZhoB0P'

conn = pymysql.connect(host='localhost',
                user='root',
                password='root',
                db='website',
                charset='utf8mb4',
                port = 8889,
                cursorclass=pymysql.cursors.DictCursor)

@app.route('/', methods=['GET'])
def home_page_get():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def home_page_post():
    airport_depart_name = request.form.get('airport_depart_name')
    airport_arrive_name = request.form.get('airport_arrive_name')
    depart_city = request.form.get('depart_city')
    arrive_city = request.form.get('arrive_city')
    depart_date = request.form.get('depart_date')
    arrive_date = request.form.get('arrive_date')
    airport_date = request.form.get('airport_date')
    city_date = request.form.get('city_date')
    flight_num = request.form.get('flight_num')

    if airport_depart_name:
        query = "SELECT * FROM flight WHERE departure_airport = '{}' AND arrival_airport = '{}' AND DATE(departure_time) = '{}'".format(airport_depart_name, airport_arrive_name, airport_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('index.html', flights1 = response)

    elif depart_city:
        query = "SELECT * FROM flight WHERE departure_airport = (SELECT airport_name FROM Airport WHERE airport_city = '{}') \
            AND arrival_airport = (SELECT airport_name FROM Airport WHERE airport_city = '{}') \
            AND DATE(departure_time) = '{}' ".format(depart_city, arrive_city, city_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('index.html', flights1 = response)

    elif flight_num:
        query = "SELECT * FROM flight WHERE flight_num = '{}' AND DATE(arrival_time) = '{}'\
            AND DATE(departure_time) = '{}'".format(flight_num, arrive_date, depart_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('index.html', flights2 = response)
        
@app.route('/register',methods = ['GET', 'POST'])
def register():
	return render_template('register.html')

@app.route('/register_customer', methods=['GET'])
def register_customer_get():
	return render_template('register_customer.html')
    
@app.route('/register_customer', methods=['POST'])
def register_customer():
    email = request.form['email']
    name = request.form['name']
    # password = request.form['password']
    building_number = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
    date_of_birth = request.form['date_of_birth']
    # Password encoded with utf-8 first then encoded with md5
    password = md5(request.form['password'].encode('utf-8')).hexdigest()
    

    query = 'SELECT * FROM Customer WHERE email="%s"' % (email)
    print(query)
    data = query_fetchone(query, conn)

    if data is not None:
        err = "User already exists!"
        flash(err)
        return redirect('/register_customer')
    else:
        query = 'INSERT INTO customer VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", ' \
                            '"{}", "{}")'.format(email, name, password, building_number, street, city, state, phone_number,\
                                    passport_number, passport_expiration, passport_country, date_of_birth)
        result = query_insert(query, conn)
        if result == 0:
            flash("Request denied, please try one more time!")
        session['email'] = email
        session['role'] = "customer"
        notification = "Successfully signed up! Please sign in again!"
        return redirect('/login_customer')

@app.route('/register_agent', methods=['GET'])
def register_agent_get():
    return render_template('register_agent.html')

@app.route('/register_agent', methods=['POST'])
def register_agent():
    email = request.form['email']
    # password = request.form['password']
    # confirm_password = request.form['confirm_password']
    # Password encoded with utf-8 first then encoded with md5
    password = md5(request.form['password'].encode('utf-8')).hexdigest()
    confirm_password = md5(request.form['confirm_password'].encode('utf-8')).hexdigest()
    if password != confirm_password:
        err = "The confirmed password should match the password you input before!"
        flash(err)
        return render_template("register_agent.html")

    booking_agent_ID = request.form['booking_agent_ID']

    query = 'SELECT * FROM Booking_agent WHERE email="%s"' % (email)
    print(query)
    data = query_fetchone(query, conn)

    if data is not None:
        err = "User already exists!"
        flash(err)
        return redirect('/register_agent')
    else:
        query = 'INSERT INTO Booking_agent VALUES("{}", "{}", "{}")'.format(email, password, booking_agent_ID)
        result = query_insert(query, conn)
        if result == 0:
            flash("Request denied, please try one more time!")
        session['email'] = email
        session['role'] = "agent"
        notification = "Successfully signed up! Please sign in again!"
        return redirect('/login_agent')

@app.route('/register_staff', methods=['GET'])
def register_staff_get():
    return render_template('register_staff.html')

@app.route('/register_staff', methods=['POST'])
def register_staff():
    username = request.form['username']
    # password = request.form['password']
    # confirm_password = request.form['confirm_password']
    password = md5(request.form['password'].encode('utf-8')).hexdigest()
    confirm_password = md5(request.form['confirm_password'].encode('utf-8')).hexdigest()
    
    if password != confirm_password:
        err = "The confirmed password should match the password you input before!"
        flash(err)
        return render_template("register_staff.html")
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    airline_name = request.form['airline_name']
    
    
    query = 'SELECT * FROM airline_staff WHERE username="%s"' % (username)
    print(query)
    data = query_fetchone(query, conn)

    if data is not None:
        err = "User already exists!"
        flash(err)
        return redirect('/register_staff')
    #elif airline_name not in query_fetchall('SELECT airline_name FROM airline', conn):
        #query_insert('INSERT INTO airline VALUES("{}")'.format(airline_name),conn)

    else:
        query = 'INSERT INTO airline_staff VALUES("{}", "{}", "{}", "{}", "{}", "{}")'.format(username, password, first_name, last_name, date_of_birth, airline_name)
        result = query_insert(query, conn)
        if result == 0:
            flash("Request denied, please try one more time!")

        session['username'] = username
        session['role'] = "staff"
        notification = "Successfully signed up! Please sign in again!"
        return redirect('/login_staff')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/login_customer', methods=['GET'])
def login_customer_get():
	return render_template('login_customer.html')

@app.route('/login_customer', methods=['POST'])
def login_customer():
    email = request.form['email']
    password = request.form['password']
    #password = md5(request.form['password'].encode('utf-8')).hexdigest()

    query = 'SELECT * FROM Customer WHERE email="%s" and password="%s"' % (email, password)
    print(query)
    data = query_fetchone(query, conn)

    if (data):
        session['email'] = email
        session['role'] = "customer"
        return redirect('/home_customer')
    else:
        err = "Email or password error!"
        flash(err)
        return redirect('/login_customer')

@app.route('/login_agent', methods=['GET'])
def login_agent_get():
	return render_template('login_agent.html')

@app.route('/login_agent', methods=['POST'])
def login_agent():
    email = request.form['email']
    #password = md5(request.form['password'].encode('utf-8')).hexdigest()
    password = request.form['password']
    query = 'SELECT * FROM Booking_agent WHERE email="%s" and password="%s"' % (email, password)
    print(query)
    data = query_fetchone(query, conn)

    if (data):
        session['email'] = email
        session['role'] = "agent"
        session['booking_agent_id']=data['booking_agent_id']
        return redirect('/home_agent')
    else:
        err = "Email or password error!"
        flash(err)
        return redirect('/login_agent')

@app.route('/login_staff', methods=['GET'])
def login_staff_get():
	return render_template('login_staff.html')

@app.route('/login_staff', methods=['POST'])
def login_staff():
    email = request.form['email']
    #password = md5(request.form['password'].encode('utf-8')).hexdigest()
    password = request.form['password']

    query = 'SELECT * FROM Airline_staff WHERE username ="%s" and password="%s"' % (email, password)
    print(query)
    data = query_fetchone(query, conn)

    if (data):
        session['email'] = email
        session['role'] = "staff"
        return redirect('/home_staff')
    else:
        err = "Email or password error!"
        flash(err)
        return redirect('/login_staff')

@app.route('/home_customer', methods=['GET'])
def customer_page_get():
	return render_template('home_customer.html')

@app.route('/home_customer', methods=['POST'])
def customer_page():
    print(session['email'])
    print(session['role'])            
    return render_template("home_customer.html", username=session['email'])

@app.route('/myflight', methods=['GET'])
def myflight_get():
    # Show my flights
    print(session['email'])
    query = "SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id  FROM purchases, Ticket natural join Flight WHERE ticket.ticket_ID = purchases.ticket_ID and purchases.customer_email = '{}' ".format(session['email'])
    print('my_flights SQL: ', query)
    my_flights = query_fetchall(query, conn)
    print(my_flights)
    print('my_flights response: ', my_flights)
    return render_template("myflight.html", flights=my_flights, username = session['email'])

@app.route('/myflight', methods=['POST'])
def myflight_post():
    # Show my flights
    query = "SELECT * FROM purchases, Ticket natural join Flight WHERE ticket.ticket_ID = purchases.ticket_ID and purchases.customer_email = '{}' ".format(session['email'])
    print('my_flights SQL: ', query)
    my_flights = query_fetchall(query, conn)
    print('my_flights response: ', my_flights)
    return render_template("myflight.html", flights=my_flights, username = session['email'])

@app.route('/myspending', methods=['GET'])
def myspending_get():
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    one_year_ago = date.today() + relativedelta(months=-12)
    six_months_ago = date.today() + relativedelta(months=-6)
    # six months spending graph
    query = "SELECT SUM(price) AS total, YEAR(purchase_date) AS y, MONTH(purchase_date) AS m FROM purchases natural join Ticket natural join flight WHERE ticket.ticket_ID = purchases.ticket_ID and ticket.flight_num = Flight.flight_num AND purchases.customer_email = '{}' AND purchases.purchase_date >= '{}' GROUP BY YEAR(purchase_date), MONTH(purchase_date)".format(session['email'], six_months_ago)
            
    
    print('six month spending SQL: ', query)
    six_months = query_fetchall(query, conn)
    six_month_sum = 0
    for i in range(len(six_months)):
        six_month_sum += float(six_months[i]["total"])
    # one year spending        
    query = "SELECT SUM(price) AS total, YEAR(purchase_date) AS y, MONTH(purchase_date) AS m FROM purchases natural join Ticket natural join flight WHERE ticket.ticket_ID = purchases.ticket_ID and ticket.flight_num = Flight.flight_num AND purchases.customer_email = '{}' AND purchases.purchase_date >= '{}' GROUP BY YEAR(purchase_date), MONTH(purchase_date)".format(session['email'], one_year_ago)
            
    print('one_year spending SQL: ', query)
    one_year = query_fetchall(query, conn)
    
    print('one_year', one_year)
    one_year_sum = 0
    for i in range(len(one_year)):
        one_year_sum += float(one_year[i]["total"])
    return render_template("myspending.html", username=session['email'],six_month_spending=six_months, one_year_spending=one_year_sum)


@app.route('/myspending', methods=['POST'])
def myspending_post():
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    one_year_ago = date.today() + relativedelta(months=-12)
    six_months_ago = date.today() + relativedelta(months=-6)
    # six months spending graph
    query = "SELECT SUM(price) AS total, YEAR(purchase_date) AS y, MONTH(purchase_date) AS m FROM purchases natural join Ticket natural join flight WHERE ticket.ticket_ID = purchases.ticket_ID and ticket.flight_num = Flight.flight_num AND purchases.customer_email = '{}' AND purchases.purchase_date >= '{}' GROUP BY YEAR(purchase_date), MONTH(purchase_date)".format(session['email'], six_months_ago)
            
    
    # print('six month spending SQL: ', query+query2)
    six_months = query_fetchall(query, conn)
    six_month_sum = 0
    for i in range(len(six_months)):
        six_month_sum += float(six_months[i]["total"])
    # one year spending        
    query = "SELECT SUM(price) AS total, YEAR(purchase_date) AS y, MONTH(purchase_date) AS m FROM purchases natural join Ticket natural join flight WHERE ticket.ticket_ID = purchases.ticket_ID and ticket.flight_num = Flight.flight_num AND purchases.customer_email = '{}' AND purchases.purchase_date >= '{}' GROUP BY YEAR(purchase_date), MONTH(purchase_date)".format(session['email'], one_year_ago)
            
    print('one_year spending SQL: ', query)
    one_year = query_fetchall(query, conn)
    
    print('one_year', one_year)
    one_year_sum = 0
    for i in range(len(one_year)):
        one_year_sum += float(one_year[i]["total"])
        
    if from_date:
        query = "SELECT SUM(price) AS total, YEAR(purchase_date) AS y, MONTH(purchase_date) AS m FROM purchases natural join Ticket natural join flight WHERE ticket.ticket_ID = purchases.ticket_ID and ticket.flight_num = Flight.flight_num AND purchases.customer_email = '{}' AND purchases.purchase_date >= '{}' AND purchases.purchase_date <= '{}' GROUP BY YEAR(purchase_date), MONTH(purchase_date)".format(session['email'], from_date,to_date)
    
        range_spending = query_fetchall(query, conn)
                
        range_sum = 0
        for i in range(len(range_spending)):
            range_sum += float(range_spending[i]["total"])

        return render_template("myspending.html", username=session['email'],six_month_spending=six_months, one_year_spending=one_year_sum,range_spending = range_spending, range_sum = range_sum)
        
    return render_template("myspending.html", username=session['email'],six_month_spending=six_months, one_year_spending=one_year_sum)


@app.route('/search_flights', methods=['GET'])
def search_flights_get():
    return render_template("search_flights.html")

@app.route('/search_flights', methods=['POST'])
def search_flights_post():
    airport_depart_name = request.form.get('airport_depart_name')
    airport_arrive_name = request.form.get('airport_arrive_name')
    depart_city = request.form.get('depart_city')
    arrive_city = request.form.get('arrive_city')
    depart_date = request.form.get('depart_date')
    arrive_date = request.form.get('arrive_date')
    airport_date = request.form.get('airport_date')
    city_date = request.form.get('city_date')
    flight_num = request.form.get('flight_num')
    if airport_depart_name:
        query = "SELECT * FROM flight WHERE departure_airport = '{}' AND arrival_airport = '{}' \
            AND DATE(departure_time) = '{}'".format(airport_depart_name, airport_arrive_name, airport_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('search_flights.html', flights1 = response)

    elif depart_city:
        query = "SELECT * FROM flight WHERE departure_airport = (SELECT airport_name FROM Airport WHERE airport_city = '{}') \
            AND arrival_airport = (SELECT airport_name FROM Airport WHERE airport_city = '{}') \
            AND DATE(departure_time) = '{}'".format(depart_city, arrive_city, city_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('search_flights.html', flights1 = response)

    elif flight_num:
        query = "SELECT * FROM flight WHERE flight_num = '{}' AND DATE(arrival_time) = '{}'\
            AND DATE(departure_time) = '{}'".format(flight_num, arrive_date, depart_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('search_flights.html', flights2 = response)
    
@app.route('/purchasing', methods=['GET'])
def purchasing_get():
    return render_template("purchasing.html",username=session['email'])

@app.route('/purchasing', methods=['POST'])
def purchasing_post():
    airline_name = request.form.get('airline_name')
    flight_number = request.form.get('flight_number')
    depart_date_time = request.form.get('depart_date_time')
    purchase_date_time = date.today()
    #calculate sold price
    #get passenger number
    if airline_name:
        query = "SELECT count(*) as total FROM Ticket natural join flight WHERE ticket.flight_num = flight.flight_num AND flight_num = '{}' AND DATE(departure_time) = '{}'\
        AND airline_name = '{}'".format(flight_number, str(depart_date_time), airline_name)
        result = query_fetchone(query, conn)
        print(result)
        passenger_num = int(result["total"])
        print("passenger_num", passenger_num)

        query_seat = "SELECT seats,price,departure_time as depart_time FROM Airplane natural join Flight WHERE Flight.airplane_id = Airplane.airplane_id AND flight_num = '{}' AND DATE(departure_time) = '{}'\
        AND airline_name = '{}'".format(flight_number, str(depart_date_time), airline_name)
        seat_query = query_fetchone(query_seat, conn)
        print(query_seat)
        print(seat_query)
        print("seat_query",seat_query)
        seat_num = int(seat_query["seats"])
        print("seat_num",seat_num)


        print("seat number:", seat_num)
        print("passenger number:", passenger_num)
        if seat_num <= passenger_num:
            flash("The flight is already full!")
            return render_template("purchasing.html",username=session['email'])
        
        sold_price = int(seat_query["price"])
        print("sold_price",sold_price)

        query1="SELECT max(ticket_id) as tid from ticket;"
        print(query1)
        result = query_fetchone(query1, conn)
        if result["tid"] == None:
            result["tid"] = 0
        print(result)
        ID=1+result["tid"]
        
        query = "INSERT INTO Ticket VALUES ('{}','{}','{}')".format(ID, airline_name, flight_number)
        result = query_fetchall(query, conn)
        
        query2 = "INSERT INTO purchases VALUES ('{}', '{}',null,'{}')".format(ID,session['email'], str(purchase_date_time))
        result = query_fetchall(query2, conn)
        return render_template("purchasing.html",username=session['email'], purchase =True )
    return render_template("purchasing.html",username=session['email'])

@app.route('/home_agent', methods=['GET'])
def agent_page_get():
    return render_template('home_agent.html',username=session['email'])

@app.route('/home_agent', methods=['POST'])
def agent_page():
    print(session['email'])
    print(session['role'])
    if session['role'] =="agent":
        return render_template("home_agent.html", username=session['email'])

    return redirect('/login')

@app.route('/agent_topcustomers', methods=['GET', 'POST'])
def agent_topcustomers():
    six_month_ago = date.today() + relativedelta(months=-6)
    one_year_ago = date.today() + relativedelta(months=-12)

    # Top 5 customers based on number of tickets bought in past 6 months
    query = "SELECT distinct name, COUNT(*) AS num_of_tickets FROM Customer, purchases NATURAL JOIN Ticket\
        WHERE Customer.email=purchases.customer_email AND booking_agent_id='{}' AND DATE(purchase_date)>='{}'\
        AND purchases.ticket_ID=ticket.ticket_ID GROUP BY name ORDER BY num_of_tickets DESC".format(session['booking_agent_id'], six_month_ago)
    print(query)
    six_month_top = query_fetchall(query, conn)
    print(six_month_top)
    for c in six_month_top:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    if len(six_month_top) < 5:
        top_customer_tkts = six_month_top
    else:
        top_customer_tkts = six_month_top[0:5]
    print(top_customer_tkts)

    # Top 5 customers based on amount of commission received in the last year
    query = "SELECT name, SUM(price)*0.1 AS sum_commission FROM Customer, purchases NATURAL JOIN Ticket NATURAL JOIN flight\
        WHERE Customer.email=purchases.customer_email AND booking_agent_id='{}' AND DATE(purchase_date)>='{}'\
        AND purchases.ticket_ID=ticket.ticket_ID GROUP BY name ORDER BY sum_commission DESC".format(session['booking_agent_id'], one_year_ago)
    print(query)
    one_year_top = query_fetchall(query, conn)
    for c in one_year_top:
        c["sum_commission"] = float(c["sum_commission"])
    print(one_year_top)
    if len(one_year_top) < 5:
        top_customer_comm = one_year_top
    else:
        top_customer_comm = one_year_top[0:5]
    print(top_customer_comm)

    labels = [ item['name'] for item in top_customer_tkts]
    datas = [ item['num_of_tickets'] for item in top_customer_tkts]
    print(labels)
    print(datas)
    return render_template("agent_topcustomers.html", username=session['email'], top_customer_tkts=top_customer_tkts,\
        top_customer_comm=top_customer_comm,label_chart = labels,data = datas)

@app.route('/agent_myflight', methods=['GET'])
def agent_myflight_get():
    print(session['email'])
    today = date.today()
    query = "SELECT DISTINCT * FROM purchases, Ticket NATURAL JOIN Flight WHERE ticket.ticket_ID = purchases.ticket_ID \
        AND purchases.booking_agent_id = '{}' AND departure_time>'{}'".format(session['booking_agent_id'], today)
    my_flights = query_fetchall(query, conn)
    print("my_flights response: ", my_flights)
    return render_template("agent_myflight.html", flights=my_flights, username=session['email'])

@app.route('/agent_mycommission', methods=['GET','POST'])
def agent_mycommission():
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    one_month_ago = date.today() + relativedelta(days=-30)

    # total amount of commission in the past 30 days
    query = "SELECT SUM(price)*0.1 AS total FROM purchases NATURAL JOIN Ticket \
        NATURAL JOIN flight \
        WHERE booking_agent_id='{}' AND DATE(purchase_date)>='{}' AND ticket.ticket_ID=purchases.ticket_ID".format(session['booking_agent_id'], one_month_ago)
    print(query)
    p30=query_fetchone(query, conn)
    print('p30',p30)
    if p30["total"] is None:
        total = 0
    else:
        total = float(p30["total"])
    print("30 days commission:", total)

    # average commission
    query2 = "SELECT COUNT(*) AS num FROM purchases NATURAL JOIN Ticket WHERE booking_agent_id='{}' \
        AND DATE(purchase_date)>='{}'AND ticket.ticket_ID=purchases.ticket_ID".format(session['booking_agent_id'], one_month_ago)
    print(query2)
    if p30["total"] is None:
        num_of_tickets = 0
        average = 0
    else:
        num_of_tickets = query_fetchone(query2, conn)["num"]
        average = total/num_of_tickets
    print("30 days number of tickets bought:", num_of_tickets)
    print("30 days average commission received:", average)

    # specift a range
    if from_date:
        query = "SELECT SUM(price)*0.1 AS total FROM purchases NATURAL JOIN Ticket \
        NATURAL JOIN flight \
        WHERE booking_agent_id='{}' AND DATE(purchase_date) between '{}' and '{}'AND ticket.ticket_ID=purchases.ticket_ID".format(session['booking_agent_id'], from_date, to_date)
        print(query)
        prange=query_fetchone(query, conn)
        print("prange",prange)
        if prange["total"] is None:
            range_total = 0.0
        else:
            range_total = float(prange["total"])
        print("Total commission:", range_total)
        if range_total ==None:
            no_comm=True
        else:
            no_comm=False
        query2 = "SELECT COUNT(*) AS num FROM purchases NATURAL JOIN Ticket WHERE booking_agent_id='{}' \
        AND DATE(purchase_date) between '{}' and '{}'AND ticket.ticket_ID=purchases.ticket_ID".format(session['booking_agent_id'], from_date, to_date)
        print(query2)
        if prange["total"] is None:
            range_num_tkts = 0.0
        else:
            range_num_tkts = query_fetchone(query2, conn)["num"]
        print("Number of tickets:", range_num_tkts)

        return render_template("agent_mycommission.html", username=session['email'], total=total, \
            num_of_tickets=num_of_tickets, average=average, range_total=range_total, range_num_tkts=range_num_tkts, show = True,no_comm = no_comm)
    return render_template("agent_mycommission.html", username=session['email'], total=total, \
            num_of_tickets=num_of_tickets, average=average)

@app.route('/agent_search', methods=['GET'])
def agent_search_get():
    return render_template("agent_search.html", username=session['email'])

@app.route('/agent_search', methods=['POST'])
def agent_search_post():
    airport_depart_name = request.form.get('airport_depart_name')
    airport_arrive_name = request.form.get('airport_arrive_name')
    depart_city = request.form.get('depart_city')
    arrive_city = request.form.get('arrive_city')
    depart_date = request.form.get('depart_date')
    arrive_date = request.form.get('arrive_date')
    airport_date = request.form.get('airport_date')
    city_date = request.form.get('city_date')
    flight_num = request.form.get('flight_num')
    if airport_depart_name:
        query = "SELECT * FROM flight WHERE departure_airport = '{}' AND arrival_airport = '{}' \
            AND DATE(departure_time) = '{}'".format(airport_depart_name, airport_arrive_name, airport_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('agent_search.html', flights1 = response, username=session['email'])

    elif depart_city:
        query = "SELECT * FROM flight WHERE departure_airport = (SELECT airport_name FROM Airport WHERE airport_city = '{}') \
            AND arrival_airport = (SELECT airport_name FROM Airport WHERE airport_city = '{}') \
            AND DATE(departure_time) = '{}'".format(depart_city, arrive_city, city_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('agent_search.html', flights1 = response, username=session['email'])

    elif flight_num:
        query = "SELECT * FROM flight WHERE flight_num = '{}' AND DATE(arrival_time) = '{}'\
            AND DATE(departure_time) = '{}'".format(flight_num, arrive_date, depart_date)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('agent_search.html', flights2 = response, username=session['email'])

@app.route('/agent_purchasing', methods=['GET'])
def agent_purchasing_get():
    return render_template("agent_purchasing.html", username=session['email'])

@app.route('/agent_purchasing', methods=['POST'])
def agent_purchasing_post():
    customer_email = request.form.get('customer_email')
    airline_name = request.form.get('airline_name')
    flight_number = request.form.get('flight_number')
    depart_date_time = request.form.get('depart_date_time')
    purchase_date_time = date.today()

    #get passenger number
    if airline_name:
        query = "SELECT count(*) as total FROM Ticket WHERE flight_num = '{}' AND airline_name = '{}'".format(flight_number, airline_name)
        result = query_fetchone(query, conn)
        print(result)
        passenger_num = int(result["total"])
        print("passenger_num", passenger_num)

        query_seat = "SELECT seats,price,departure_time as depart_time FROM Airplane natural join Flight \
            WHERE Flight.airplane_id = Airplane.airplane_ID AND flight_num = '{}' AND DATE(departure_time) = '{}'\
            AND airline_name = '{}'".format(flight_number, str(depart_date_time), airline_name)
        print(query_seat)
        seat_query = query_fetchone(query_seat, conn)
        print(seat_query)
        print("seat_query",seat_query)
        if seat_query is None:
            seat_num = 0
        else:
            seat_num = int(seat_query["seats"])
        print("seat_num",seat_num)

        if seat_num <= passenger_num:
            flash("The flight is already full!")
            return render_template("agent_purchasing.html", username=session['email'])

        sold_price = int(seat_query["price"])
        
        query1="SELECT max(ticket_id) as tid from ticket;"
        print(query1)
        result = query_fetchone(query1, conn)
        print(result)
        ID=1+result["tid"]

        query="SELECT * from customer where email='{}'".format(customer_email)
        print(query)
        customer_query = query_fetchone(query, conn)
        print(customer_query)
        if customer_query is None:
            flash("Customer not exist! Register first!")
            return render_template("agent_purchasing.html", username=session['email'])
        else:
            query2 = "INSERT INTO Ticket VALUES ('{}', '{}', '{}')".format(ID, airline_name, flight_number)
            print(query2)
            result = query_fetchall(query2, conn)

            query3 = "INSERT INTO purchases VALUES ('{}', '{}', '{}', '{}')".format(ID,customer_email, session['booking_agent_id'],str(purchase_date_time))
            print(query3)
            result = query_fetchall(query3, conn)

        return render_template("agent_purchasing.html", username=session['email'], purchase=True)
    return render_template("agent_purchasing.html", username=session['email'])


@app.route('/home_staff', methods=['GET'])
def staff_page_get():
	return render_template('home_staff.html', username=session['email'])

@app.route('/home_staff', methods=['POST'])
def staff_page():
    print(session['email'])
    print(session['role'])            
    return render_template("home_staff.html", username=session['email'])


@app.route('/staff_search_flight', methods=['GET'])
def staff_search_flight_get():
    one_months_next = date.today() + relativedelta(months=+1)
    date_today = date.today()
    # Show airline flights
    print(session['email'])
    query = "SELECT * FROM Flight natural join Airline_staff WHERE username = '{}'and departure_time>'{}' and departure_time<'{}'".format(session['email'],date_today, one_months_next)
    airline_flights = query_fetchall(query, conn)
    print(airline_flights)
    return render_template("staff_search_flight.html", flights=airline_flights, username = session['email'])

@app.route('/staff_search_flight', methods=['POST'])
def staff_search_flight_post():
    # Show airline flights
    print(session['email'])
    query = "SELECT * FROM Flight natural join Airline_staff WHERE username = '{}' ".format(session['email'])
    airline_flights = query_fetchall(query, conn)
    print(airline_flights)
    #search flights
    airport_depart_name = request.form.get('airport_depart_name')
    airport_arrive_name = request.form.get('airport_arrive_name')
    depart_city = request.form.get('depart_city')
    arrive_city = request.form.get('arrive_city')
    depart_date = request.form.get('depart_date')
    arrive_date = request.form.get('arrive_date')
    airport_date = request.form.get('airport_date')
    city_date = request.form.get('city_date')
    flight_num = request.form.get('flight_num')
    
    customer_depart_date_time = request.form.get('customer_depart_date_time')
    customer_flight_num = request.form.get('customer_flight_number')
    customer_airline_name = request.form.get('customer_airline_name')
    
    status_depart_date_time = request.form.get('status_depart_date_time')
    status_flight_num = request.form.get('status_flight_number')
    status_airline_name = request.form.get('status_airline_name')
    
    if airport_depart_name:
        query = "SELECT * FROM flight natural join Airline_staff WHERE departure_airport = '{}' AND arrival_airport = '{}' \
            AND DATE(departure_time) = '{}' AND username = '{}'".format(airport_depart_name, airport_arrive_name, airport_date,session['email'])
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('staff_search_flight.html',  flights=airline_flights, flights1 = response,username = session['email'])
    elif depart_city:
        query = "SELECT * FROM flight natural join Airline_staff WHERE departure_airport = (SELECT airport_name FROM Airport WHERE airport_city = '{}') \
            AND arrival_airport = (SELECT airport_name FROM Airport WHERE airport_city = '{}') \
            AND DATE(departure_time) = '{}' AND username = '{}'".format(depart_city, arrive_city, city_date,session['email'])
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('staff_search_flight.html', flights=airline_flights,  flights1 = response,username = session['email'])
    elif flight_num:
        query = "SELECT * FROM flight natural join Airline_staff WHERE flight_num = '{}' AND DATE(arrival_time) = '{}'\
            AND DATE(departure_time) = '{}' AND username = '{}'".format(flight_num, arrive_date, depart_date,session['email'])
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('staff_search_flight.html',  flights=airline_flights, flights2 = response,username = session['email'])
    # search for status
    elif status_flight_num:
        query = "SELECT status FROM flight WHERE flight_num = '{}' AND DATE(departure_time) = '{}' AND airline_name = '{}'".format(status_flight_num, status_depart_date_time, status_airline_name)
        print(query)
        response = query_fetchall(query, conn)
        print(response[0]["status"])
        return render_template('staff_search_flight.html',  flights=airline_flights, flights_status = response[0]["status"],username = session['email'])
    # search for customer number
    elif customer_flight_num:
        query = "SELECT count(*) as num FROM flight natural join ticket WHERE flight_num = '{}' AND DATE(departure_time) = '{}' AND airline_name = '{}'".format(customer_flight_num, customer_depart_date_time, customer_airline_name)
        print(query)
        response = query_fetchall(query, conn)
        print(response)
        return render_template('staff_search_flight.html',  flights=airline_flights, flight_customer = response[0]["num"], username = session['email'])
    return render_template('staff_search_flight.html')



@app.route('/staff_update_flights', methods=['GET'])
def staff_update_flights_get():
    if session['role'] != 'staff':
        err = "You are not a staff!"
        print( session['role'])
        flash(err)
        return redirect('/login_staff')
    else:
        #get airline name of the staff
        query_airline = "SELECT airline_name FROM Airline_staff WHERE username = '{}' ".format(session['email'])
        staff_airline =  query_fetchone(query_airline, conn)
        staff_airline_name = staff_airline["airline_name"]
        print("staff_airline_name",staff_airline_name)
        #get airplane of the airline
        query = "SELECT * FROM Flight where airline_name = '{}'".format(staff_airline_name)
        all_airplane = query_fetchall(query, conn)
        print("all airplane",all_airplane)
        return render_template("staff_update_flights.html", all_airplane = all_airplane, staff_airline_name = staff_airline_name, username = session['email'])

@app.route('/staff_update_flights', methods=['POST'])
def staff_update_flights_post():
    #get airline name of the staff
    query_airline = "SELECT airline_name FROM Airline_staff WHERE username = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    print("staff_airline_name",staff_airline_name)
    #create flights
    create_airline_name = request.form.get('create_airline_name')
    create_flight_number = request.form.get('create_flight_number')
    create_airline_id = request.form.get('create_airline_id')
    create_depart_date_time = request.form.get('create_depart_date_time')
    create_arrival_date_time = request.form.get('create_arrival_date_time')
    create_airport_depart_name = request.form.get('create_airport_depart_name')
    create_airport_arrival_name = request.form.get('create_airport_arrival_name')
    create_status = request.form.get('create_status')
    create_base_price = request.form.get('create_base_price')
    #change flight status
    status_depart_date_time = request.form.get('status_depart_date_time')
    status_flight_num = request.form.get('status_flight_number')
    status_airline_name = request.form.get('status_airline_name')
    status_status = request.form.get('status_status')   
    #add airplane
    add_airplane_id = request.form.get('add_airplane_id')
    add_num_of_seats = request.form.get('add_num_of_seats')
    add_airline_name = request.form.get('add_airline_name')
    #add airport
    airport_name = request.form.get('airport_name')
    airport_city = request.form.get('airport_city')
    
    if session['role'] != 'staff':
        err = "You are not a staff!"
        print( session['role'])
        flash(err)
        return redirect('/login_staff')
    else:
        if create_airline_name:
        #insert new flight
            query = 'INSERT INTO Flight VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(create_airline_name, create_flight_number, create_airport_depart_name, create_depart_date_time, create_airport_arrival_name, create_arrival_date_time, create_base_price, create_status,create_airline_id)
            result = query_insert(query, conn)
            if result == 0:
                flash("Request denied, please try one more time!")
            return render_template("staff_update_flights.html", staff_airline_name = staff_airline_name, username = session['email'],update = True)
        elif status_flight_num:
            query = 'UPDATE Flight SET status = "{}" WHERE airline_name= "{}" AND flight_num = "{}" AND DATE(departure_time) = "{}" '.format(status_status, status_airline_name, status_flight_num, status_depart_date_time)
            result = query_insert(query, conn)
            print("change status",query)
            print(result)
            if result == 0:
                flash("No flight exists!")
            return render_template("staff_update_flights.html", staff_airline_name = staff_airline_name, username = session['email'],update = True)
        elif add_airplane_id:
            query = 'INSERT INTO Airplane VALUES("{}", "{}", "{}")'.format(add_airline_name, add_airplane_id, add_num_of_seats)
            result = query_insert(query, conn)
            print("add airplane",query)
            print(result)
            if result == 0:
                flash("Unable to add flight!")
            return render_template("staff_update_flights.html", staff_airline_name = staff_airline_name, username = session['email'],update = True)
        elif airport_city:
            query = 'INSERT INTO Airport VALUES("{}", "{}")'.format(airport_name, airport_city)
            result = query_insert(query, conn)
            print("add airport",query)
            print(result)
            if result == 0:
                flash("Unable to add airport!")
            return render_template("staff_update_flights.html", staff_airline_name = staff_airline_name, username = session['email'],update = True)
        else:
            return render_template("staff_update_flights.html", staff_airline_name = staff_airline_name, username = session['email'],update = False)

@app.route('/staff_revenue', methods=['GET'])
def staff_revenue_get():
    query_airline = "SELECT airline_name FROM Airline_staff WHERE username = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    labels = []
    today = date.today()
    one_month_ago = today + relativedelta(months=-1)
    one_year_ago = today + relativedelta(years=-1)
    # Direct sales in the last month
    query1 = "SELECT SUM(price) AS v FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE airline_name = '{}' \
        AND purchase_date BETWEEN '{}' AND '{}' AND booking_agent_id is NULL".format(staff_airline_name, one_month_ago, today)
    print(query1)
    result = query_fetchall(query1, conn)
    print(result)
    print(result[0]['v'])
    if result[0]['v'] == None:
        result[0]['v']  =0
    labels.extend(result)
    
    # Indirect sales in the last month
    query2 = "SELECT SUM(price) AS v FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE airline_name = '{}' \
        AND purchase_date BETWEEN '{}' AND '{}' And booking_agent_id is not NULL".format(staff_airline_name, one_month_ago, today)
    print(query2)
    result = query_fetchall(query2, conn)
    if result[0]['v']   == None:
        result[0]['v']  =0
    labels.extend(result)
        
    # Direct sales in the last year
    query3 = "SELECT SUM(price) AS v FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE airline_name = '{}' \
        AND purchase_date BETWEEN '{}' AND '{}' and booking_agent_id is NULL".format(staff_airline_name, one_year_ago, today)
    print(query3)
    result = query_fetchall(query3, conn)
    if result[0]['v']  == None:
        result[0]['v']  =0
    labels.extend(result)
    
    # Indirect sales in the last year
    query4 = "SELECT SUM(price) AS v FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE airline_name = '{}' \
        AND purchase_date BETWEEN '{}' AND '{}' and booking_agent_id is not NULL".format(staff_airline_name, one_year_ago, today)
    print(query4)
    result = query_fetchall(query4, conn)
    if result[0]['v']   == None:
        result[0]['v']  =0
    labels.extend(result)
    
    for value in labels:
        value['v'] = float(value['v'])
    print(labels)
    
    return render_template("staff_revenue.html", staff_airline_name = staff_airline_name, username = session['email'], labels = labels)

@app.route('/staff_allagents', methods=['GET'])
def staff_allagents_get():
    one_month_ago = date.today() + relativedelta(months=-1)
    one_year_ago = date.today() + relativedelta(months=-12)
    query_airline = "SELECT airline_name FROM Airline_staff WHERE username = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    # Top 5 agents based on the number of tickets sales for the past month
    query = "SELECT distinct booking_agent_id, COUNT(*) AS num_of_tickets FROM purchases NATURAL JOIN Ticket\
        WHERE airline_name='{}' AND DATE(purchase_date)>='{}' AND booking_agent_id is not null GROUP BY booking_agent_id ORDER BY num_of_tickets DESC".format(staff_airline_name, one_month_ago)
    print(query)
    one_month_top = query_fetchall(query, conn)
    for c in one_month_top:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    if len(one_month_top) < 5:
        top_agent_tkts = one_month_top
    else:
        top_agent_tkts = one_month_top[0:5]
    print(top_agent_tkts)

    # Top 5 agents based on the number of tickets sales for the past year
    query = "SELECT distinct booking_agent_id, COUNT(*) AS num_of_tickets FROM purchases NATURAL JOIN Ticket\
        WHERE airline_name='{}' AND DATE(purchase_date)>='{}' AND booking_agent_id is not null GROUP BY booking_agent_id ORDER BY num_of_tickets DESC".format(staff_airline_name,one_year_ago)
    print(query)
    tkts_one_year_top = query_fetchall(query, conn)
    for c in tkts_one_year_top:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    if len(tkts_one_year_top) < 5:
        top_agent_tkts_year = tkts_one_year_top
    else:
        top_agent_tkts_year = tkts_one_year_top[0:5]
    print(top_agent_tkts_year)

    # Top 5 agents based on the amount of commission received for the last year
    query = "SELECT booking_agent_id, SUM(price)*0.1 AS sum_commission FROM purchases NATURAL JOIN Ticket Natural Join flight\
        WHERE airline_name='{}' AND DATE(purchase_date)>='{}' AND booking_agent_id is not null GROUP BY booking_agent_id ORDER BY sum_commission DESC".format(staff_airline_name,one_year_ago)
    print(query)
    one_year_top = query_fetchall(query, conn)
    for c in one_year_top:
        c["sum_commission"] = float(c["sum_commission"])
    #print(one_year_top)
    if len(one_year_top) < 5:
        top_agent_comm = one_year_top
    else:
        top_agent_comm = one_year_top[0:5]
    print(top_agent_comm)

    return render_template("staff_allagents.html", username=session['email'], top_agent_tkts=top_agent_tkts, \
        top_agent_tkts_year=top_agent_tkts_year, top_agent_comm=top_agent_comm)

@app.route('/staff_destination', methods=['GET'])
def staff_destination_get():
    three_month_ago = date.today() + relativedelta(months=-3)
    one_year_ago = date.today() + relativedelta(months=-12)
    today_date = date.today()
    query_airline = "SELECT airline_name FROM Airline_staff WHERE username = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    # Top 3 popular destination in past 3 months (based on number of tickets bought)
    query = "SELECT distinct airport_city, COUNT(*) AS num_of_tickets FROM Airport, Flight NATURAL JOIN purchases NATURAL JOIN ticket\
        WHERE ticket.airline_name = '{}' and arrival_airport = Airport.airport_name AND DATE(departure_time)>='{}' AND DATE(purchase_date)<='{}' GROUP BY 1 ORDER BY num_of_tickets DESC".format(staff_airline_name,three_month_ago,today_date)
    print(query)
    three_month_top = query_fetchall(query, conn)
    #print(six_month_top)
    for c in three_month_top:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    if len(three_month_top) < 3:
        top_destination_three_month = three_month_top
    else:
        top_destination_three_month = three_month_top[0:3]
    print(top_destination_three_month)

    # Top 3 popular destination in last year (based on number of tickets bought)
    query = "SELECT distinct airport_city, COUNT(*) AS num_of_tickets FROM Airport, Flight NATURAL JOIN purchases NATURAL JOIN ticket\
        WHERE ticket.airline_name = '{}' and arrival_airport = Airport.airport_name AND DATE(departure_time)>='{}' AND DATE(purchase_date)<='{}'  GROUP BY 1 ORDER BY num_of_tickets DESC".format(staff_airline_name,one_year_ago,today_date)
    one_year_top = query_fetchall(query, conn)
    for c in one_year_top:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    if len(one_year_top) < 3:
        top_destination_one_year = one_year_top
    else:
        top_destination_one_year = one_year_top[0:3]
    
    return render_template("staff_destination.html", username=session['email'], top_destination_one_year=top_destination_one_year,\
        top_destination_three_month=top_destination_three_month)

@app.route('/staff_destination', methods=['POST'])
def staff_destination_post():
    return render_template("staff_destination.html",username=session['email'])

@app.route('/staff_view_report', methods=['GET'])
def sstaff_view_report_get():
    one_year_ago = date.today() + relativedelta(months=-12)
    today_date = date.today()
    query_airline = "SELECT airline_name FROM Airline_staff WHERE username = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    # report in past year
    query = "SELECT COUNT(*) AS num_of_tickets, YEAR(purchase_date) AS y, MONTH(purchase_date) AS m FROM purchases NATURAL JOIN ticket \
        WHERE airline_name = '{}' and purchase_date >= '{}' AND purchase_date <= '{}' GROUP BY YEAR(purchase_date), MONTH \
        (purchase_date)".format(staff_airline_name,one_year_ago,today_date)
    print(query)
    one_year_tkt = query_fetchall(query, conn)
    for c in one_year_tkt:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    print(one_year_tkt)

    return render_template("staff_view_report.html", username=session['email'], one_year_tkt=one_year_tkt)

@app.route('/staff_view_report', methods=['POST'])
def staff_view_report_post():
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    one_year_ago = date.today() + relativedelta(months=-12)
    today_date = date.today()
    query_airline = "SELECT airline_name FROM Airline_staff WHERE username = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    # report in past year
    query = "SELECT COUNT(*) AS num_of_tickets, YEAR(purchase_date) AS y, MONTH(purchase_date) AS m FROM purchases NATURAL JOIN ticket \
        WHERE airline_name = '{}' and purchase_date >= '{}' AND purchase_date <= '{}' GROUP BY YEAR(purchase_date), MONTH \
        (purchase_date)".format(staff_airline_name,one_year_ago,today_date)
    print(query)
    one_year_tkt = query_fetchall(query, conn)
    for c in one_year_tkt:
        c["num_of_tickets"] = int(c["num_of_tickets"])
    print(one_year_tkt)

    # report in a specified range
    if from_date:
        query = "SELECT COUNT(*) AS num_of_tickets, YEAR(purchase_date) AS y, MONTH(purchase_date) AS m FROM purchases NATURAL JOIN ticket \
        WHERE airline_name = '{}' and purchase_date >= '{}' AND purchase_date <= '{}' GROUP BY YEAR(purchase_date), MONTH \
        (purchase_date)".format(staff_airline_name,from_date,to_date)
        print(query)
        range_tkt = query_fetchall(query, conn)
        for c in range_tkt:
            c["num_of_tickets"] = int(c["num_of_tickets"])
        print(one_year_tkt)

    return render_template("staff_view_report.html",username=session['email'], one_year_tkt=one_year_tkt, range_tkt=range_tkt)


@app.route('/staff_frequent_customer', methods=['GET'])
def staff_frequent_customer_get():
    #most frequent customer
    one_year_ago = date.today() + relativedelta(months=-12)
    query_airline = "SELECT airline_name FROM Airline_staff WHERE username = '{}' ".format(session['email'])
    staff_airline =  query_fetchone(query_airline, conn)
    staff_airline_name = staff_airline["airline_name"]
    print(session['email'])
    query = "SELECT distinct customer_email, count(*) as num_of_tickets FROM purchases, Ticket WHERE airline_name='{}' and purchases.ticket_ID = Ticket.ticket_ID AND purchase_date>='{}' GROUP BY customer_email".format(staff_airline_name,one_year_ago)
    cust_buy_tkt = query_fetchall(query, conn)
    print(cust_buy_tkt)                   
    max_cust = cust_buy_tkt[0]
    for item in cust_buy_tkt:
        if item['num_of_tickets']>=max_cust['num_of_tickets']:
            max_cust = item
            
    #see flights of a particular customer on particular airline   
    query = "SELECT * FROM purchases, Ticket natural join Flight WHERE ticket.ticket_ID = purchases.ticket_ID and airline_name = '{}' ".format(staff_airline_name)
    print('my_flights SQL: ', query)
    cust_flights = query_fetchall(query, conn)
    print('cust_flights response: ', cust_flights)
    
    return render_template("/staff_frequent_customer.html", flights=cust_flights,staff_airline_name = staff_airline_name,  max_cust = max_cust, username = session['email'])

@app.route('/staff_frequent_customer', methods=['POST'])
def staff_frequent_customer_post():
    return render_template('/staff_frequent_customer.html', username = session['email'])

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    session.pop('role', None)
    return redirect("/login")


if __name__ == "__main__":
    app.run('127.0.0.1', 5000)

