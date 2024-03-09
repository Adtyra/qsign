from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class VTTD():
    def __init__(self, id_t, namafile,hvalue, pkey, tsign, id_p):
        self.id_t =  id_t
        self.namafile =  namafile
        self.hvalue =  hvalue
        self.pkey = pkey
        self.tsign = tsign
        self.id_p = id_p 

    def __repr__(self):
        return '<Ttd %r>' % self.id_t

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

    @classmethod
    def create(cls, conn, id_t, namafile,hvalue, pkey, tsign, id_p):
        cursor = conn.connection.cursor()
        cursor.execute('''INSERT INTO tb_ttd (id_t, namafile,hvalue, pkey, tsign, id_p) VALUES (%s, %s, %s, %s, %s, %s)''', (id_t, namafile,hvalue, pkey, tsign, id_p))
        conn.connection.commit()
        cursor.close()
    
   # @classmethod
   # def timeto(cls, conn, id_t, hashfile, ttdx, timecek,wat):
#        cursor = conn.connection.cursor()
#        cursor.execute('''INSERT INTO tb_time (id_t, hashfile, ttdx, timecek,wat) VALUES (%s, %s, %s,  %s,  %s)''', (id_t, hashfile, ttdx, timecek,wat))
        #conn.connection.commit()
        #cursor.close()
    
    @classmethod
    def get_all(cls, conn):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_ttd''')
        ttd = cursor.fetchall()
        cursor.close()
        return ttd

    @classmethod
    def get_by_id_user(cls, conn, id_p):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_ttd WHERE id_p = %s''', (id_p,))
        ttd = cursor.fetchall()
        cursor.close()
        return ttd

    @classmethod
    def get_by_id_sign(cls, conn, id_t):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_ttd WHERE id_t = %s''', (id_t,))
        ttd = cursor.fetchone()
        cursor.close()
        return ttd

    @classmethod
    def get_by_hash(cls, conn, hvalue):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_ttd WHERE hvalue = %s''', (hvalue,))
        ttd = cursor.fetchone()
        cursor.close()
        return ttd
    
    @classmethod
    def update(cls, conn, id_t, namafile,hvalue, pkey, tsign, id_p):
        cursor = conn.connection.cursor()
        cursor.execute('''UPDATE tb_ttd SET namafile= %s, hvalue= %s, pkey = %s, tsign = %s, id_p = %s WHERE id_t = %s''', ( namafile,hvalue, pkey, tsign,id_p, id_t))
        conn.connection.commit()
        cursor.close()

    @classmethod
    def delete(cls, conn, id):
        cursor = conn.connection.cursor()
        cursor.execute('''DELETE FROM tb_ttd WHERE id = %s''', (id,))
        conn.connection.commit()
        cursor.close()

class VDK():
    def __init__(self, id_k, namauser, kuncipublik, id_p):
        self.id_k =  id_k
        self.namauser =  namauser
        self.kuncipublik = kuncipublik
        self.id_p = id_p

    def __repr__(self):
        return '<DK %r>' % self.id_k

    @classmethod
    def create(cls, conn, id_k, namauser, kuncipublik, id_p):
        cursor = conn.connection.cursor()
        cursor.execute('''INSERT INTO tb_dk (id_k, namauser, kuncipublik, id_p) VALUES (%s, %s, %s, %s)''', (id_k, namauser, kuncipublik, id_p))
        conn.connection.commit()
        cursor.close()

    @classmethod
    def get_all(cls, conn):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_dk''')
        dk = cursor.fetchall()
        cursor.close()
        return dk

    @classmethod
    def get_by_id_p(cls, conn, id_p):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_dk WHERE id_p = %s''', (id_p,))
        dk = cursor.fetchall()
        cursor.close()
        return dk

    @classmethod
    def get_by_id_key(cls, conn, id_k):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_dk WHERE id_k = %s''', (id_k,))
        ttd = cursor.fetchone()
        cursor.close()
        return ttd

    @classmethod
    def update(cls, conn, id_k, namauser, kuncipublik, id_p):
        cursor = conn.connection.cursor()
        cursor.execute('''UPDATE tb_dk SET namauser= %s, kuncipublik = %s, id_p = %s WHERE id_k = %s''', ( namauser, kuncipublik, id_p, id_k))
        conn.connection.commit()
        cursor.close()

    @classmethod
    def delete(cls, conn, id_k):
        cursor = conn.connection.cursor()
        cursor.execute('''DELETE FROM tb_dk WHERE id_k = %s''', (id_k,))
        conn.connection.commit()
        cursor.close()

class STTD():
    def __init__(self, mid, filename, hvalue,sigkey, skey, pkey, nsig, uid1, tsig1, uid2, tsig2, uid3, tsig3, uid4, tsig4 ):
        self.mid        =  mid
        self.filename   =  filename
        self.hvalue     =  hvalue
        self.sigkey     =  sigkey
        self.skey       =  skey
        self.pkey       =  pkey
        self.nsig       =  nsig
        self.uid1       =  uid1
        self.tsig1      =  tsig1
        self.uid2       =  uid2
        self.tsig2      =  tsig2
        self.uid3       =  uid3
        self.tsig3      =  tsig3
        self.uid4       =  uid4
        self.tsig4      =  tsig4

    def __repr__(self):
        return '<sttd %r>' % self.mid

    @classmethod
    def create(cls, conn, mid, filename, hvalue,sigkey, skey, pkey, nsig, nsed, uid1, tsig1, uid2, tsig2, uid3, tsig3, uid4, tsig4):
        cursor = conn.connection.cursor()
        cursor.execute('''INSERT INTO tb_sttd (mid, filename, hvalue,sigkey, skey, pkey, nsig,nsed, uid1, tsig1, uid2, tsig2, uid3, tsig3, uid4, tsig4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (mid, filename, hvalue,sigkey, skey, pkey, nsig, nsed, uid1, tsig1, uid2, tsig2, uid3, tsig3, uid4, tsig4))
        conn.connection.commit()
        cursor.close()
    
    @classmethod
    def get_by_id_sign(cls, conn, mid):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_sttd WHERE mid = %s''', (mid,))
        ttd = cursor.fetchone()
        cursor.close()
        return ttd
    
    @classmethod
    def get_by_hash(cls, conn, hvalue):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_sttd WHERE hvalue = %s''', (hvalue,))
        ttd = cursor.fetchone()
        cursor.close()
        return ttd
    
    @classmethod
    def get_by_id1(cls, conn, uid1):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_sttd WHERE uid1 = %s''', (uid1,))
        mttd1 = cursor.fetchall()
        cursor.close()
        return mttd1
    
    @classmethod
    def get_by_id2(cls, conn, uid2):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_sttd WHERE uid2 = %s''', (uid2,))
        mttd2 = cursor.fetchall()
        cursor.close()
        return mttd2
    
    @classmethod
    def get_by_id3(cls, conn, uid3):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_sttd WHERE uid3 = %s''', (uid3,))
        mttd3 = cursor.fetchall()
        cursor.close()
        return mttd3
    
    @classmethod
    def get_by_id4(cls, conn, uid4):
        cursor = conn.connection.cursor()
        cursor.execute('''SELECT * FROM tb_sttd WHERE uid4 = %s''', (uid4,))
        mttd4 = cursor.fetchall()
        cursor.close()
        return mttd4
    
    @classmethod
    def update(cls, conn, mid, filename, hvalue, sigkey, skey, pkey, nsig, nsed, uid1, tsig1, uid2, tsig2, uid3, tsig3, uid4, tsig4):
        cursor = conn.connection.cursor()
        cursor.execute('''UPDATE tb_sttd SET filename= %s, hvalue = %s,sigkey =%s, skey = %s, pkey = %s,  nsig = %s, nsed = %s, uid1 = %s, tsig1 = %s, uid2 = %s, tsig2 = %s, uid3 = %s, tsig3 = %s, uid4 = %s, tsig4 = %s  WHERE mid = %s''', ( filename, hvalue,sigkey, skey, pkey, nsig, nsed, uid1, tsig1, uid2, tsig2, uid3, tsig3, uid4, tsig4, mid ))
        conn.connection.commit()
        cursor.close()