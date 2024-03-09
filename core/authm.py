from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import check_password_hash, generate_password_hash

class User(UserMixin):
    def __init__(self, id_p, email, nama,  password, foto, bio, kunci_privat, kunci_publik, hidemail):
        self.id_p =  id_p
        self.email =  email
        self.nama =  nama
        self.password = password
        self.foto = foto
        self.bio = bio
        self.kunci_privat = kunci_privat
        self.kunci_publik = kunci_publik
        self.hidemail = hidemail
    def __repr__(self):
        return '<User %r>' % self.id_p

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

    @classmethod
    def create(cls, conn, id_p, email, nama, password, foto, bio, kunci_privat, kunci_publik, hidemail):
        cursor = conn.connection.cursor()
        cursor.execute('''INSERT INTO tb_pengguna (id_p, email, nama, password, foto, bio, kunci_privat, kunci_publik, hidemail) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)''', (id_p, email, nama,  password, foto, bio, kunci_privat, kunci_publik,hidemail))
        conn.connection.commit()
        cursor.close()

    @classmethod
    def get_all(cls, conn):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_pengguna''')
        user = cursor.fetchall()
        cursor.close()
        return user

    @classmethod
    def get_by_id(cls, conn, id_p):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_pengguna WHERE id_p = %s''', (id_p,))
        user = cursor.fetchone()
        cursor.close()
        return user

    @classmethod
    def get_by_email(cls, conn, email):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_pengguna WHERE email = %s''', (email,))
        user = cursor.fetchone()
        cursor.close()
        return user
        
    @classmethod
    def update(cls, conn, id_p, email, nama,  password, foto, bio, kunci_privat, kunci_publik,hidemail):
        cursor = conn.connection.cursor()
        cursor.execute('''UPDATE tb_pengguna SET email= %s, nama = %s, password = %s, foto = %s, bio = %s, kunci_privat = %s, kunci_publik = %s,hidemail =%s WHERE id_p = %s''', (email, nama, password, foto, bio, kunci_privat, kunci_publik, hidemail,id_p))
        conn.connection.commit()
        cursor.close()

    @classmethod
    def updateprofil(cls, conn, id_p, email, nama, password, foto, bio, nkunci_privat, nkunci_publik,hidemail):
        cursor = conn.connection.cursor()
        cursor.execute('''UPDATE tb_pengguna SET email= %s, nama = %s, password = %s, foto = %s, bio = %s, kunci_privat = %s, kunci_publik = %s,hidemail =%s WHERE id_p = %s''', (email, nama, password, foto, bio, nkunci_privat, nkunci_publik,hidemail,id_p))
        conn.connection.commit()                                                                                                                                           
        cursor.close()

    @classmethod
    def store(cls, conn, id_p, email, nama, password, foto, bio, kunci_privat, kunci_publik,hidemail):
        cursor = conn.connection.cursor()
        cursor.execute('''INSERT INTO tb_pengguna (id_p, email, nama, password, foto, bio, kunci_privat, kunci_publik,hidemail) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (id_p ,email, nama, password, foto, bio, kunci_privat, kunci_publik,hidemail))
        conn.connection.commit()
        cursor.close()

    @classmethod
    def delete(cls, conn, id):
        cursor = conn.connection.cursor()
        cursor.execute('''DELETE FROM tb_pengguna WHERE id = %s''', (id,))
        conn.connection.commit()
        cursor.close()

    @classmethod
    def get_by_username(cls, conn, email):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_pengguna WHERE email = %s''', (email,))
        user = cursor.fetchone()
        cursor.close()
        return user



class ModelUser():
    @classmethod
    def logged(self, conn, user):
        try:
            cursor = conn.connection.cursor()
            cursor.execute('''SELECT * FROM tb_pengguna WHERE email = %s''', (user.email,))
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], row[2], row[3], User.check_password(row[4], user.password), row[5], row[6], row[7], row[8])
                cursor.close()
                return user
            else:
                cursor.close()
                return None
        except Exception as ex:
            raise Exception(ex)