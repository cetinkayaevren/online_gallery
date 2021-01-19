from flask import Flask, abort, render_template, current_app, request, redirect, url_for,flash, session, send_from_directory
from datetime import datetime
from forms import LoginForm, CustomerRegisterForm, SellerRegisterForm, AddCar
from passlib.hash import sha256_crypt
from flask_login import logout_user,login_user, login_required, current_user
import psycopg2
import psycopg2.extras
import io
from datetime import datetime
from PIL import Image
import base64
import shutil
from functools import wraps
from werkzeug.utils import secure_filename
import sys
import os
#from PIL import Image
from io import BytesIO
import glob



#conn = psycopg2.connect(host = "localhost", database="gallery_system", user = "postgres", password = "12bizimkiler34")
os.environ['DATABASE_URL'] = 'postgres://phnwhvksewajsz:a90858a6b71e057c3c557b5b4f9cc7c2b12f2e0b78bc81f1082a587fe92c49a0@ec2-54-76-215-139.eu-west-1.compute.amazonaws.com:5432/d7labpo9324rt8'
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

ABSOLUTE_PATH = os.path.abspath('./uploaded_files')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
count = 0
app = Flask(__name__)



def connect_to_db():
    try:
        return psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        print("Cannot connect to the database !")


def is_logged(a):
    @wraps(a)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return a(*args, **kwargs)
        else:
            flash("Unauthorized, Log in or Register", 'danger')
            return redirect(url_for('login_customer_page'))
    return wrap

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day = day_name)

@is_logged
def cars_page():

    conn = connect_to_db()
    cur = conn.cursor()

    if request.method == "GET":
        try:
            cur.execute("SELECT cars.car_brand, cars.car_model, cars.car_year, online_market.price, online_market.sell_rent, online_market.title, seller_account.seller_province, online_market.product_id,seller_account.account_type FROM((cars INNER JOIN online_market ON cars.product_no = online_market.product_id) INNER JOIN seller_account ON cars.owner_id = seller_account.seller_id) ORDER BY seller_account.account_type DESC")
        except:
            print("Error executing select")
        results = cur.fetchall()
        return render_template("cars.html", my_results = results)

    else:
        conn = connect_to_db()
        cur = conn.cursor()
        cars = None
        my_option = request.form.get("sorted_by")
        if my_option == '2':
            return redirect(url_for('cars_page'))
        if my_option == '0':
            try:
                cur.execute("SELECT cars.car_brand, cars.car_model, cars.car_year, online_market.price, online_market.sell_rent, online_market.title, seller_account.seller_province, online_market.product_id,seller_account.account_type FROM((cars INNER JOIN online_market ON cars.product_no = online_market.product_id) INNER JOIN seller_account ON cars.owner_id = seller_account.seller_id) ORDER BY online_market.price")
                cars = cur.fetchall()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for('cars_page'))
        if my_option == '1':
            try:
                cur.execute("SELECT cars.car_brand, cars.car_model, cars.car_year, online_market.price, online_market.sell_rent, online_market.title, seller_account.seller_province, online_market.product_id,seller_account.account_type FROM((cars INNER JOIN online_market ON cars.product_no = online_market.product_id) INNER JOIN seller_account ON cars.owner_id = seller_account.seller_id) ORDER BY online_market.price DESC")
                cars = cur.fetchall()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for('cars_page'))

        if my_option == '3':
            try:
                cur.execute("SELECT cars.car_brand, cars.car_model, cars.car_year, online_market.price, online_market.sell_rent, online_market.title, seller_account.seller_province, online_market.product_id,seller_account.account_type FROM((cars INNER JOIN online_market ON cars.product_no = online_market.product_id) INNER JOIN seller_account ON cars.owner_id = seller_account.seller_id) ORDER BY cars.car_year DESC")
                cars = cur.fetchall()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for('cars_page'))

        if my_option == '4':
            try:
                cur.execute("SELECT cars.car_brand, cars.car_model, cars.car_year, online_market.price, online_market.sell_rent, online_market.title, seller_account.seller_province, online_market.product_id,seller_account.account_type FROM((cars INNER JOIN online_market ON cars.product_no = online_market.product_id) INNER JOIN seller_account ON cars.owner_id = seller_account.seller_id) ORDER BY seller_account.seller_province")
                cars = cur.fetchall()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for('cars_page'))

        return render_template("cars.html", my_results = cars)

def download_file(filename):
    return send_from_directory(ABSOLUTE_PATH, filename, as_attachment = False)

@is_logged
def car_page(car_key):
    filelist = glob.glob(os.path.join(ABSOLUTE_PATH,"*"))
    for f in filelist:
        os.remove(f)
    global count
    #os.remove(filename)
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT cars.car_brand, cars.car_model, cars.car_year, cars.fuel_type, cars.km, cars.photo, online_market.price, online_market.sell_rent, online_market.title, online_market.description, seller_account.seller_province, online_market.product_id, seller_account.seller_name, seller_account.seller_surname, seller_account.seller_telephone, reliability_ratio.ratio, seller_account.seller_id FROM(((cars INNER JOIN online_market ON cars.product_no = online_market.product_id ) INNER JOIN seller_account ON cars.owner_id = seller_account.seller_id) INNER JOIN reliability_ratio ON seller_account.seller_id = reliability_ratio.account_no) WHERE online_market.product_id = {car_key}")
    except:
        print("Error executing select")
    """ Car Image
        cur.execute(f"SELECT * FROM cars WHERE product_no = {inserted_id}")
        result = cur.fetchone()
    """
    file_name = 'my_car_image'+str(count)+'.png'
    results = cur.fetchall()
    stream = BytesIO(results[0][5])
    filename = os.path.join(ABSOLUTE_PATH, file_name)  # I assume you have a way of picking unique filenames
    image = Image.open(stream)
    #send_from_directory(ABSOLUTE_PATH, filename, as_attachment = True)
    image.save(filename)
    file_name1 = 'my_car_image'+str(count-1)+'.png'
    filename2 = os.path.join(ABSOLUTE_PATH, file_name1)  # I assume you have a way of picking unique filenames
    try:
        os.remove(filename2)
    except:
        pass

    if results is None:
        abort(404)
    cur.close()
    #count +=1
    #print(file_name)
    #print(filename)
    #print(file_name1)
    #print(filename2)
    return render_template("car.html", my_car=results, image_name = file_name, car_key = car_key)


def login_entry():
    return render_template('login_entry.html')

def login_customer_page():
    if request.method == 'POST':
        email = request.form['email']
        password_written = request.form['password']
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM customer_account WHERE customer_mail = '{email}'")
        data = cur.fetchone()
        if data is not None :
            password = data[5]
            if sha256_crypt.verify(password_written, password):
                session['logged_in'] = True
                session["logged_as"] = "customer"
                session['username'] = email
                session['id'] = data[0]
                session['name'] = data[2]

                flash(f'You are now logged in as {data[2]}', 'success')
                return redirect(url_for('home_page'))
            else:
                flash('Invalid Password')
                return render_template('login_customer.html')
            cur.close()
        else:
            flash("Username not found")
            return render_template('login_customer.html')
    return render_template("login_customer.html")

def login_seller_page():
    if request.method == 'POST':
        email = request.form['email']
        password_written = request.form['password']
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM seller_account WHERE seller_mail = '{email}'")
        data = cur.fetchone()
        if data is not None :
            password = data[5]
            if sha256_crypt.verify(password_written, password):
                session['logged_in'] = True
                session["logged_as"] = "seller"
                session['username'] = email
                session['id'] = data[0]
                session['name'] = data[2]

                flash(f'You are now logged in as {data[2]}', 'success')
                return redirect(url_for('home_page'))
            else:
                flash('Invalid Password')
                return render_template('login_seller.html')
            cur.close()
        else:
            flash("Username not found")
            return render_template('login_seller.html')
    return render_template("login_seller.html")

def register_entry():
    return render_template('register_entry.html')

def customer_register_page():
    form = CustomerRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data 
        password = sha256_crypt.encrypt(str(form.password.data))
        citizen_id = form.citizen_id.data
        customer_age = form.customer_age.data
        customer_province = form.customer_province.data
        customer_telephone = form.customer_telephone.data
        register_time = datetime.now()

        conn = connect_to_db()
        cur = conn.cursor()
        try:
            cur.execute(f"INSERT INTO customer(customer_citizen_id) values({citizen_id});")
            conn.commit()
        except psycopg2.Error as e:
            flash(e.pgerror)
        try:
            cur.execute(f"INSERT INTO customer_account(citizen_id, customer_name, customer_surname, customer_mail, customer_password, customer_age, customer_province, customer_telephone, register_date, reliability_count) values('{citizen_id}','{name}','{surname}','{email}','{password}',{customer_age},'{customer_province}','{customer_telephone}','{register_time}',3);")
            conn.commit()
            flash("Register Operation is Success !!", 'success')
            return redirect(url_for('home_page'))
        except psycopg2.Error as e:
            pass
        cur.close()
        return redirect(url_for("customer_register_page"))
    return render_template('customer_register.html', form = form)

def seller_register_page():
    form = SellerRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        account_type = request.form.get('account_type')
        if(account_type == "0"):
            account_type=False
        else:
            account_type=True
        name = form.seller_name.data
        surname = form.seller_surname.data
        email = form.email.data 
        password = sha256_crypt.encrypt(str(form.password.data))
        seller_citizen_id = form.citizen_id.data
        seller_age = form.seller_age.data
        seller_province = form.seller_province.data
        seller_telephone = form.seller_telephone.data
        register_time = datetime.now()

        conn = connect_to_db()
        cur = conn.cursor()
        try:
            cur.execute(f"INSERT INTO seller(seller_citizen_id) values({seller_citizen_id});")
            conn.commit()
        except psycopg2.Error as e:
            flash(e.pgerror)
        try:
            cur.execute(f"INSERT INTO seller_account(person_id, seller_name, seller_surname, seller_mail, seller_password, seller_age, seller_province, seller_telephone, account_type, register_time) values('{seller_citizen_id}','{name}','{surname}','{email}','{password}',{seller_age},'{seller_province}','{seller_telephone}','{account_type}','{register_time}');")
            conn.commit()
            cur.execute(f"SELECT seller_id FROM seller_account WHERE seller_mail = '{email}';")
            results = cur.fetchone()
            cur.execute(f"INSERT INTO reliability_ratio(account_no, number_of_votes, ratio) values({results[0]}, 0, 5.0)")
            conn.commit()
            if account_type ==False:
                cur.execute(f"INSERT INTO standard_seller(vendor_no, car_number) values({results[0]}, '{False}')")
                conn.commit()
            else:
                cur.execute(f"INSERT INTO premium_seller(supplier_no, cars_number) values({results[0]}, {0})")
                conn.commit()
            flash("Register Operation is Success !!", 'success')
            return redirect(url_for('home_page'))
        except psycopg2.Error as e:
            flash(e.pgerror)
        cur.close()
        return redirect(url_for("seller_register_page"))
    return render_template('seller_register.html',form = form)

def view_profile():
    if request.method == 'GET':
        conn = connect_to_db()
        cur = conn.cursor()
        if session["logged_as"] == "customer":
            try:
                cur.execute(f"SELECT * FROM customer_account WHERE customer_id = '{session['id']}'")
            except:
                flash("ERROR WHILE VIEWING THIS PROFILE!!")
        if session["logged_as"] == "seller":
            try:
                cur.execute(f"SELECT * FROM seller_account INNER JOIN reliability_ratio ON seller_account.seller_id = reliability_ratio.account_no WHERE seller_account.seller_id = {session['id']}")
            except:
                flash("ERROR WHILE VIEWING THIS PROFILE!!")
        data = cur.fetchone()
        cars = None
        try:
            cur.execute(f"SELECT cars.car_brand, cars.car_model, cars.car_year, cars.fuel_type, cars.car_year, cars.km, cars.product_no FROM cars WHERE cars.owner_id = '{session['id']}'")
            cars = cur.fetchall()
        except:
            cars=None
            pass
        if cars==None:
                cur.close()
                return render_template('view_profile.html',data = data, account = session["logged_as"],cars = None)
        cur.close()
        return render_template('view_profile.html',data = data, account = session["logged_as"],cars = cars)
    if request.method == 'POST':
        conn = connect_to_db()
        cur = conn.cursor()
        if session["logged_as"] == "customer":
            cur.execute(f"SELECT citizen_id FROM customer_account WHERE customer_id = {session['id']}")
            data = cur.fetchone()
            cur.execute(f"DELETE FROM customer_account WHERE customer_id = {session['id']}")
            conn.commit()
            cur.execute(f"DELETE FROM customer WHERE customer_citizen_id = '{data[0]}'")
            conn.commit()
            flash("The account is successfully deleted..")
        else:
            try:
                cur.execute(f"SELECT product_no FROM cars WHERE owner_id = {session['id']}")
                data = cur.fetchall()
                for i in range(len(data)):
                    cur.execute(f"DELETE FROM online_market WHERE product_id = {data[i][0]}")
                    conn.commit()
                cur.execute(f"DELETE FROM cars WHERE owner_id = {session['id']}")
                conn.commit()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for("home_page"))
            try:
                cur.execute(f"SELECT person_id, account_type FROM seller_account WHERE seller_id = {session['id']}")
                result = cur.fetchone()
                if result[1] == True:
                    cur.execute(f"DELETE FROM premium_seller WHERE supplier_no = {session['id']}")
                    conn.commit()
                else:
                    cur.execute(f"DELETE FROM standard_seller WHERE vendor_no = {session['id']}")
                    conn.commit()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for("home_page"))
            try:
                cur.execute(f"DELETE FROM reliability_ratio WHERE account_no = {session['id']}")
                conn.commit()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for("home_page"))
            try:
                cur.execute(f"DELETE FROM seller_account WHERE seller_id = {session['id']}")
                conn.commit()
                cur.execute(f"DELETE FROM seller WHERE seller_citizen_id = '{result[0]}'")
                conn.commit()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for("home_page"))

            flash("The account is successfully deleted..")
        logout_page()
        return redirect(url_for("home_page"))


def seller_page(key_id, seller_key):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM seller_account INNER JOIN reliability_ratio ON seller_account.seller_id = reliability_ratio.account_no WHERE seller_account.seller_id = '{seller_key}'")
    except:
        flash("ERROR WHILE VIEWING THIS PROFILE!!")

    data = cur.fetchone()
    
    if request.method == 'GET':

        cars = None
        try:
            cur.execute(f"SELECT cars.car_brand, cars.car_model, cars.car_year, cars.fuel_type, cars.car_year, cars.km FROM cars WHERE cars.owner_id = '{seller_key}'")
            cars = cur.fetchall()
        except:
            cars=None
            pass
        if cars==None:
            cur.close()
            return render_template('view_seller_profile.html',data = data, account = "seller",cars = None)
        cur.close()
        return render_template('view_seller_profile.html',data = data, account = "seller",cars = cars)
    else:
        cur.execute(f"SELECT reliability_count FROM customer_account WHERE customer_id = {session['id']}")
        counter=cur.fetchone()[0]
        if(counter == 0):
            flash("You have no any vote right !")
            return redirect(url_for('seller_page',key_id = key_id, seller_key = seller_key))
        else:
            ratio = int(request.form.get('reliability'))
            number_of_votes = int(data[13])
            main_ratio = float(data[14])
            new_result = round(((main_ratio*number_of_votes) + ratio)/(number_of_votes + 1),2)
            number_of_votes = number_of_votes + 1
            cur.execute(f"UPDATE reliability_ratio SET number_of_votes = {number_of_votes}, ratio = {new_result} WHERE account_no = {seller_key}")
            conn.commit()
            counter = counter - 1
            cur.execute(f"UPDATE customer_account SET reliability_count = {counter} WHERE customer_id = {session['id']}")
            conn.commit()
            flash("Your vote successfully committed !")
            cur.close()
            return redirect(url_for('seller_page',key_id = key_id, seller_key = seller_key))

def return_image(stream):
    bytes_stream = BytesIO(stream)
    img = Image.open(bytes_stream).convert("RGBA")
    return img

def read_binary(pic):
    with open(pic, mode='rb') as f:
        #print(f)
        my_byte = f.read()
        return my_byte

def allowed_images(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_car():
    #BASE_PATH = os.path.abspath(os.environ.get('HOME'))

    form = AddCar(request.form)
    if request.method == 'POST' and form.validate():
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(f"SELECT car_number FROM standard_seller WHERE vendor_no = {session['id']}")
        account_type = cur.fetchone()

        if account_type != None and account_type[0] == True:
            flash("You cannot add more than one car in online market because you are standard seller")
            return redirect(url_for('add_car'))
        brand = form.brand.data 
        model = form.model.data 
        year = form.year.data 
        sell_rent = form.sell_rent.data
        title = form.title.data
        province = form.province.data
        price = form.price.data
        fuel_type = form.fuel_type.data
        km = form.km.data
        text = request.form.get('text_write')
        file = request.files['pic']

        if(file.filename == ''):
            flash('No file is selected')
            return redirect(url_for('add_car'))
        
        if(allowed_images(file.filename) == False):
            flash('Image format is not appropriate !!')
            return redirect(url_for('add_car'))

        filename = secure_filename(file.filename)
        file.save(os.path.join(ABSOLUTE_PATH, filename))
        #file.save(os.path.join(r'./uploaded_files', file.filename))
        new_file = os.path.join(ABSOLUTE_PATH, filename)

        data = read_binary(new_file)

        #readed_byte = file.read()
        try:
            cur.execute(f"INSERT INTO cars (owner_id, car_brand, car_model, fuel_type, km, car_year, photo) VALUES ({session['id']}, '{brand}', '{model}', '{fuel_type}', '{km}', '{year}', %s) returning product_no", (data, ))
            inserted_id = cur.fetchone()[0]
            conn.commit()
            if(sell_rent == "0"):
                sell_rent = True
            else:
                sell_rent=False
            cur.execute(f"INSERT INTO online_market (product_id, price, sell_rent, title, description) VALUES ({inserted_id}, {price}, {sell_rent}, '{title}', '{text}');")
            conn.commit()
        except psycopg2.Error as e:
            flash(e.pgerror)
            return redirect(url_for('add_car'))
        os.remove(new_file)

        if account_type == None:
            cur.execute(f"UPDATE premium_seller SET cars_number = cars_number + 1 WHERE supplier_no = {session['id']}")
            conn.commit()
        else:
            try:
                cur.execute(f"UPDATE standard_seller SET car_number = {True} WHERE vendor_no = {session['id']}")
                conn.commit()
            except psycopg2.Error as e:
                flash(e.pgerror)                

        flash("Your Car Has Been Published !!")
    return render_template('add_car.html', form = form)

def delete_cars(prod_no):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute(f"DELETE FROM online_market WHERE product_id = {prod_no}")
        conn.commit()
    except psycopg2.Error as e:
        flash(e.pgerror)
        return redirect(url_for('view_profile'))
    try:
        cur.execute(f"DELETE FROM cars WHERE product_no = {prod_no}")
        conn.commit()
    except psycopg2.Error as e:
        flash(e.pgerror)
        return redirect(url_for('view_profile'))
    try:
        cur.execute(f"SELECT account_type FROM seller_account WHERE seller_id = {session['id']}")
        data = cur.fetchone()
    except psycopg2.Error as e:
        flash(e.pgerror)
        return redirect(url_for('view_profile'))

    if data[0] == True:
        cur.execute(f"UPDATE premium_seller SET cars_number = cars_number - 1 WHERE supplier_no = {session['id']}")
        conn.commit()
    else:
        cur.execute(f"UPDATE standard_seller SET car_number = {False} WHERE vendor_no = {session['id']}")
        conn.commit()
    flash("Your Car is Deleted Successfully !")
    return redirect(url_for("view_profile"))

def update_accounts():
    if request.method == 'POST':
        conn = connect_to_db()
        cur = conn.cursor()
        if session['logged_as'] == "customer":
            cur.execute(f"SELECT customer_mail, customer_age, customer_province, customer_telephone FROM customer_account WHERE customer_id = {session['id']}")
        else:
            cur.execute(f"SELECT seller_mail, seller_age, seller_province, seller_telephone FROM seller_account WHERE seller_id = {session['id']}")
        data = cur.fetchone()
        new_email = request.form.get('email')
        new_age = request.form.get('age')
        new_province = request.form.get('province')
        new_telephone = request.form.get('telephone')
        if new_email == '':
            new_email = data[0]
        if new_age == '':
            new_age = data[1]
        if new_province == '':
            new_province = data[2]
        if new_telephone == '':
            new_telephone = data[3]
        if session["logged_as"] == "customer":
            try:
                cur.execute(f"UPDATE customer_account SET customer_mail = '{new_email}', customer_age = {new_age}, customer_province = '{new_province}', customer_telephone = '{new_telephone}' WHERE customer_id = {session['id']}")
                conn.commit()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for('update_accounts'))
        else:
            try:
                cur.execute(f"UPDATE seller_account SET seller_mail = '{new_email}', seller_age = {new_age}, seller_province = '{new_province}', seller_telephone = '{new_telephone}' WHERE seller_id = {session['id']}")
                conn.commit()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for('update_accounts'))
        flash("Your Account Informations are Updated Successfully !")
        return redirect(url_for('view_profile'))
    return render_template("update_accounts.html")

def update_cars(prod_no):
    if request.method == 'POST':
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(f"SELECT cars.fuel_type, cars.km, online_market.sell_rent, online_market.price, online_market.title, online_market.description FROM cars INNER JOIN online_market ON cars.product_no = online_market.product_id WHERE cars.product_no = {prod_no}")
        data = cur.fetchone()
        fuel_type = request.form.get('fueltype')
        new_km = request.form.get('km')
        sell_rent = request.form.get('sell_rent')
        new_price = request.form.get('price')
        new_title = request.form.get('title')
        new_text = request.form.get('text_write')
        if sell_rent == '0':
            sell_rent = True
        if sell_rent == '1':
            sell_rent = False
        if fuel_type == '':
            fuel_type = data[0]
        if new_km == '':
            new_km = data[1]
        if sell_rent == '2':
            sell_rent = data[2]
        if new_price == '':
            new_price = data[3]
        if new_title == '':
            new_title = data[4]
        if new_text == '':
            new_text = data[5]
        try:
            cur.execute(f"UPDATE cars SET fuel_type = '{fuel_type}', km = {new_km} WHERE product_no = {prod_no}")
            conn.commit()
        except psycopg2.Error as e:
            flash(e.pgerror)
            return redirect(url_for('update_cars', prod_no = prod_no))
        try:
            cur.execute(f"UPDATE online_market SET sell_rent = {sell_rent}, price = {new_price}, title = '{new_title}', description = '{new_text}' WHERE product_id = {prod_no}")
            conn.commit()
        except psycopg2.Error as e:
            flash(e.pgerror)
            return redirect(url_for('update_cars', prod_no = prod_no))
        flash("Update Operation is success !!")
        return redirect(url_for('view_profile'))
    return render_template('update_cars.html')

def sort_cars():
    if request.method == "GET":
        conn = connect_to_db()
        cur = conn.cursor()
        cars = None
        my_option = request.form.get("sorted_by")
        if my_option == '2':
            return redirect(url_for('cars_page'))
        if my_option == '0':
            try:
                cur.execute("SELECT cars.car_brand, cars.car_model, cars.car_year, online_market.price, online_market.sell_rent, online_market.title, seller_account.seller_province, online_market.product_id,seller_account.account_type FROM((cars INNER JOIN online_market ON cars.product_no = online_market.product_id) INNER JOIN seller_account ON cars.owner_id = seller_account.seller_id) ORDER BY online_market.price")
                cars = cur.fetchall()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for('cars_page'))
        if my_option == '1':
            try:
                cur.execute("SELECT cars.car_brand, cars.car_model, cars.car_year, online_market.price, online_market.sell_rent, online_market.title, seller_account.seller_province, online_market.product_id,seller_account.account_type FROM((cars INNER JOIN online_market ON cars.product_no = online_market.product_id) INNER JOIN seller_account ON cars.owner_id = seller_account.seller_id) ORDER BY online_market.price DESC")
                cars = cur.fetchall()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for('cars_page'))

        if my_option == '3':
            try:
                cur.execute("SELECT cars.car_brand, cars.car_model, cars.car_year, online_market.price, online_market.sell_rent, online_market.title, seller_account.seller_province, online_market.product_id,seller_account.account_type FROM((cars INNER JOIN online_market ON cars.product_no = online_market.product_id) INNER JOIN seller_account ON cars.owner_id = seller_account.seller_id) ORDER BY cars.car_year DESC")
                cars = cur.fetchall()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for('cars_page'))

        if my_option == '4':
            try:
                cur.execute("SELECT cars.car_brand, cars.car_model, cars.car_year, online_market.price, online_market.sell_rent, online_market.title, seller_account.seller_province, online_market.product_id,seller_account.account_type FROM((cars INNER JOIN online_market ON cars.product_no = online_market.product_id) INNER JOIN seller_account ON cars.owner_id = seller_account.seller_id) ORDER BY seller_account.seller_province")
                cars = cur.fetchall()
            except psycopg2.Error as e:
                flash(e.pgerror)
                return redirect(url_for('cars_page'))

    return render_template("home.html")

def logout_page():
    session.clear()
    flash("You have logged out.","success")
    return redirect(url_for("home_page"))