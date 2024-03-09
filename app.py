from flask import Flask, render_template, request, redirect, url_for, flash,Blueprint, flash, g, session,send_file,send_from_directory
from core.extension import mysql, init_db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from core.authm import User,ModelUser
from flask_mysqldb import MySQL
from core.authm import User
import os
from flask_mobility import Mobility

UPLOAD_FOLDER_FILE = "static/upload/file"
UPLOAD_FOLDER_FOTO = "static/upload/foto"
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}



app = Flask(__name__)
app.auto_find_instance_path
app.config['SECRET_KEY'] = "adfladfadfdafadfafad"
# Hosting Switch ^ and v
# app.config['SECRET_KEY'] = os.urandom(32)
app.config['UPLOAD_FOLDER_FILE'] = UPLOAD_FOLDER_FILE
app.config['UPLOAD_FOLDER_FOTO'] = UPLOAD_FOLDER_FOTO
mysql=init_db(app)
Mobility(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
from core import auth,views,qsign
app.register_blueprint(auth.bp)
app.register_blueprint(views.bp)
app.register_blueprint(qsign.bp)

    
@login_manager.user_loader
def load_user(user_id):
        return User.get(User.id_p==user_id)
        
def page_not_found(e):
        return render_template('403.html'), 403

app.register_error_handler(403,page_not_found)
if __name__ == '__main__':
   app.run(debug=True)