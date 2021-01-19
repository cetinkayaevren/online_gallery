from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, Form
from wtforms.validators import NumberRange, Optional, InputRequired,Length, Email, DataRequired, EqualTo
from wtforms_components import IntegerField

from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=30)])

    password = PasswordField("Password", validators=[DataRequired(), Length(min = 8, max=40)])

    remember = BooleanField("Remember Me")

class CustomerRegisterForm(Form):
    name = StringField('Customer Name*', validators = [Length(min = 1, max = 50)])
    surname = StringField('Customer Surname*', validators = [Length(min = 1, max = 50)])
    email = StringField('E-mail*', validators = [Length(min = 1, max = 50)])
    password = PasswordField("Password*", validators=[EqualTo('confirm', message = 'Password do not match!') ,Length(min = 8, max=40)])
    confirm = PasswordField('Confirm Password')
    citizen_id = StringField('Citizen ID*', validators = [Length(min = 11, max = 11)])
    customer_age = IntegerField('Age*', validators = [NumberRange(min=18, max=110)])
    customer_province = StringField('Province*', validators = [Length(min = 3, max = 20)])
    customer_telephone = StringField('Telephone Number (without 0)*', validators = [ Length(min = 10, max = 10)])


class SellerRegisterForm(Form):
    seller_name = StringField('Seller Name*', validators = [Length(min = 1, max = 50)])
    seller_surname = StringField('Seller Surname*', validators = [Length(min = 1, max = 50)])
    email = StringField('E-mail*', validators = [Length(min = 1, max = 50)])
    password = PasswordField("Password*", validators=[EqualTo('confirm', message = 'Password do not match!') ,Length(min = 8, max=40)])
    confirm = PasswordField('Confirm Password')
    citizen_id = StringField('Citizen ID*', validators = [Length(min = 11, max = 11)])
    seller_age = IntegerField('Age*', validators = [NumberRange(min=18, max=110)])
    seller_province = StringField('Province*', validators = [Length(min = 3, max = 20)])
    seller_telephone = StringField('Telephone Number (without 0)*', validators = [ Length(min = 10, max = 10)])
    account_type = BooleanField('Account Type*', validators = [DataRequired()])

class AddCar(Form):
    brand = StringField('Brand*', validators = [Length(min = 1, max = 20)])
    model = StringField('Model*', validators = [Length(min = 1, max = 20)])
    year = IntegerField('Year*', validators = [NumberRange(min = 1945, max = 2021)])
    sell_rent = BooleanField("Sell/Rent*", validators = [DataRequired()])
    title = StringField('Please Enter Your Title*', validators = [Length(min = 5, max = 50)])
    province = StringField('Province*', validators = [Length(min = 3, max = 20)])
    price = IntegerField('Price*', validators = [NumberRange(min=100, max=999999999)])
    fuel_type = StringField('Fuel Type*', validators = [Length(min = 3, max = 20)])
    km = IntegerField('KM*',  validators = [NumberRange(min=1, max=999999)])
    #text = StringField('Please enter your text about your car*', validators = [Length(min = 1, max = 200)])



