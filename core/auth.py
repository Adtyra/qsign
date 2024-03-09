import functools
import random
import uuid as uuid
from core.authm import User,ModelUser
from flask_mysqldb import MySQL
from core.extension import mysql
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from ecdsa import SigningKey,NIST256p
import os

bp = Blueprint('auth', __name__)

UPLOAD_FOLDER_FILE = "static/upload/file"
UPLOAD_FOLDER_FOTO = "static/upload/foto"
UPLOAD_FOLDER_TEMP = "static/upload/temp"

@bp.route('/login', methods=['GET', 'POST'])
def login():
  
    return render_template('login.html')

@bp.route('/masuk', methods=['GET', 'POST'])
def masuk():
        if request.method =='POST':
            email = request.form['email']
            password = request.form['password']
            # check if user exists
            user = User.get_by_username(mysql, email)
            # if user exists
            if user:
                if check_password_hash(user['password'], password):
                    session['loggedin'] = True
                    session['id']       = user['id_p']
                    session['email']    = user['email']
                    session['nama']     = user['nama']
                    session['foto']     = user['foto']
                    session['hml']      = user['hidemail']
                    session['sk']       = user['kunci_privat']
                    session['vk']       = user['kunci_publik']
                    session['id_k']     =   ''
                    return redirect(url_for('views.index'))                
                else:
                    # return login with error
                    flash('Password Salah','warning')
                    return render_template('login.html')
            else:
                # return login with error
                flash('Akun Tidak Ditemukan','danger')
                return render_template('login.html')
        return render_template("login.html")
        
@bp.route('/logout')
#@login_required
def logout():
   # logout_user()
    try:
        session.pop('loggedin', None)
    except Exception:
        pass
    try:
        session.pop('email', None)
    except Exception:
        pass
    try:
        session.pop('nama', None)
    except Exception:
        pass
    try:
        session.pop('foto', None)
    except Exception:
        pass
    try:
        session.pop('hml', None)
    except Exception:
        pass
    try:
        session.pop('sk', None)
    except Exception:
        pass
    try: 
        session.pop('vk', None)
    except Exception:
        pass
    try:
        session.pop('id_k', None)
    except Exception:
        pass
    try:
        session.pop('qsign', None)
    except Exception:
        pass
    try:
        vfile   = session['vttd']
        dfile   = os.path.join(UPLOAD_FOLDER_FILE, vfile)
        os.remove(dfile)
    except Exception:
        pass
    try:
        tfile   = session['id']
        mfile   = os.path.join(UPLOAD_FOLDER_TEMP, tfile)
        os.remove(mfile)
    except Exception:
        pass
    try:    
        session.pop('id', None)
    except Exception:
        pass
    try:
        session.pop('tempfile', None)
    except Exception:
        pass
    try:
        session.pop('vttd', None)
    except Exception:
        pass
    try:
        session.pop('other', None)
    except Exception:
        pass
    session.clear()
    return redirect(url_for('auth.login'))

@bp.route('/clear', methods=['GET', 'POST'])
def clear():
    session['loggedin'] = ''
    session['id']       = ''
    session['email']    = ''
    session['nama']     = ''
    session['foto']     = ''
    session['hml']      = ''
    session['sk']       = ''
    session['vk']       = ''
    session['id_k']     = ''
    session.clear()
    return render_template("login.html")
    
@bp.route('/daftar', methods=['GET', 'POST'])
def sign_up():
    daftarfl="0"
    return render_template("daftar.html",dfl=daftarfl)

@bp.route('/buat', methods=['GET', 'POST'])
def buat():
    if request.method == 'POST':
        id1             = random.randint(0,99)
        id2             = random.randint(0,99)
        id3             = random.randint(0,9)
        id4             = random.randint(0,99)
        id5             = random.randint(0,99)
        id_x            = str(id1)+str(id2)+str(id3)+str(id4)+str(id5)
        userid          = User.get_by_id(mysql, id_x)
        while userid != None:
            id1             = random.randint(0,99)
            id2             = random.randint(0,99)
            id3             = random.randint(0,9)
            id4             = random.randint(0,99)
            id5             = random.randint(0,99)
            id_x            = str(id1)+str(id2)+str(id3)+str(id4)+str(id5)
            userid      = User.get_by_id(mysql, id_x)
            if userid == None:
                break
       
        id_p            = int(id_x) 
        email1          = request.form['email']
        email           = request.form.get("email")
        userx           = User.get_by_email(mysql, email)
        if userx != None: # the query has returned a user
            daftarfl = "1"
            flash("Email Telah Terdaftar, Silahkan Gunakan Email Lain")
            return render_template("daftar.html",dfl = daftarfl)    
            
        nama1           = request.form['name']
        password1       = request.form['password']
        import re
        password = request.form.get("password")

        if (len(password1)<=7):
            daftarfl = "2"
            flash("Minimal Sandi 8 Karakter")
            return render_template("daftar.html",dfl = daftarfl,nm =nama1, em =email)         
        if not re.search("[a-z]", password):
            daftarfl = "2"
            flash("Sandi Harus Mengandung Huruf Kecil")
            return render_template("daftar.html",dfl = daftarfl,nm =nama1, em =email)    
        if not re.search("[A-Z]", password):
            daftarfl = "2"
            flash("Sandi Harus Mengandung Huruf Kapital")
            return render_template("daftar.html",dfl = daftarfl,nm =nama1, em =email)    
        if not re.search("[0-9]", password):
            daftarfl = "2"
            flash("Sandi Harus Mengandung Angka")
            return render_template("daftar.html",dfl = daftarfl,nm =nama1, em =email)    
        if not re.search("[_@?<>!#$%^&*()-+\/]" , password):
            daftarfl = "2"
            flash("Sandi Harus Mengandung Karakter Spesial []_@?<>!#$%^&*()-+\/")
            return render_template("daftar.html",dfl = daftarfl,nm =nama1, em =email)    
        if re.search("\s" , password):
            daftarfl = "2"
            flash("Sandi Tidak Boleh Menggunakan Spasi")
            return render_template("daftar.html",dfl = daftarfl,nm =nama1, em =email)   
        
        foto            = 'default.png'
        bio             = 'Pemilik akun belum menulis bio'
        sk              = SigningKey.generate(curve=NIST256p)
        vk              = sk.verifying_key
        kunci_privat    = sk.to_pem()
        kunci_publik    = vk.to_pem()
        hidemail        = '0'
        User.store(mysql, id_p ,email1, nama1, generate_password_hash(password), foto, bio, kunci_privat, kunci_publik, hidemail)
        return redirect(url_for('auth.login'))
    return render_template("daftar.html")