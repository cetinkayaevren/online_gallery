from flask import Flask, render_template
from flask_login import LoginManager
from datetime import datetime
import views
from dbinit import create_database

from user import get_user
import os



lm = LoginManager()
@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/cars", view_func=views.cars_page, methods=["GET", "POST"])
    app.add_url_rule("/cars/<int:car_key>", view_func=views.car_page)
    app.add_url_rule("/customer_register", view_func=views.customer_register_page, methods=["GET", "POST"])
    app.add_url_rule("/seller_register", view_func=views.seller_register_page, methods=["GET", "POST"])
    app.add_url_rule("/register_entry", view_func = views.register_entry, methods=["GET", "POST"])
    app.add_url_rule("/login_entry", view_func = views.login_entry, methods=["GET", "POST"])
    app.add_url_rule("/view_profile", view_func = views.view_profile, methods=["GET", "POST"])
    app.add_url_rule("/cars/<int:key_id>/<int:seller_key>", view_func = views.seller_page, methods=["GET", "POST"])
    app.add_url_rule("/add_car", view_func = views.add_car, methods=["GET", "POST"])
    app.add_url_rule("/uploads/<path:filename>", view_func = views.download_file, methods=["GET", "POST"])
    app.add_url_rule("/delete_cars/<int:prod_no>", view_func = views.delete_cars, methods=["GET", "POST"])
    app.add_url_rule("/update", view_func = views.update_accounts, methods=["GET", "POST"])
    app.add_url_rule("/update_car/<int:prod_no>", view_func = views.update_cars, methods=["GET", "POST"])
    app.add_url_rule("/sort_cars", view_func = views.sort_cars, methods=["GET", "POST"])


    app.add_url_rule("/login_customer", view_func=views.login_customer_page, methods=["GET", "POST"])
    app.add_url_rule("/login_seller", view_func=views.login_seller_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)

    lm.init_app(app)
    lm.login_view = "login_customer_page"

    create_database()

    return app


if __name__ == "__main__":
    app= create_app()
    app.secret_key = 'secret123123'
    app.run(host = "0.0.0.0", port = 8080, debug = True)