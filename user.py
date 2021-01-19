from flask import current_app
from flask_login import UserMixin
import views

class User(UserMixin):
    def __init__(self, customer_id, citizen_id, name, surname, mail, password, age, province, telephone, date):
        self.cust_id = customer_id
        self.cit_id = citizen_id
        self.name = name
        self.surname = surname
        self.mail = mail
        self.password = password
        self.age = age
        self.province = province
        self.telephone = telephone
        self.date = date
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.name

    @property
    def is_active(self):
        return self.active

def get_user(user_id):

    conn = views.connect_to_db()
    cur = conn.cursor()
    print("giris")
    print(user_id)
    try:
        cur.execute(f"SELECT * FROM customer_account WHERE(customer_mail = '{user_id}')")
    except:
        print("Error executing select")
        return None
    results = cur.fetchall()

    print(results)
    password = results[0][5]

    user = User(results[0][0],results[0][1] ,results[0][2],results[0][3],results[0][4],results[0][5],results[0][6], results[0][7], results[0][8], results[0][9]) if password else None
    if user is not None:
        user.is_admin = user.mail in current_app.config["ADMIN_USERS"]
    return user