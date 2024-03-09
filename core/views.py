from flask import Blueprint, render_template, request, flash, jsonify,redirect, url_for, send_file, session,send_from_directory
import hashlib
from ecdsa import SigningKey,VerifyingKey,BadSignatureError,NIST256p
from ecdsa.util import sigencode_der, sigdecode_der
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import time
import tempfile
from core.extension import mysql
from core.qsign import qrgen
from core.msign import mgen 
from core.csign import cgen
from core.authm import User
from core.viewsm import VTTD, VDK, STTD


bp = Blueprint('views', __name__)
UPLOAD_FOLDER_FILE = "static/upload/file"
UPLOAD_FOLDER_FOTO = "static/upload/foto"
UPLOAD_FOLDER_TEMP = "static/upload/temp"

@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template("1index.html")
@bp.route('/index', methods=['GET', 'POST'])
def index2():
    return render_template("1index.html")
  
@bp.route('/pengguna', methods=['GET', 'POST'])
def pengguna(): 
    try:
        id_other = session['other']
        user     = User.get_by_id(mysql,id_other)
        session.pop('other', None)
        return render_template("2pengguna.html",user=user)
    except:
         return render_template('403.html'), 403

@bp.route('/profil', methods=['GET', 'POST'])
def profil(): 
    if 'loggedin' in session:
            from ecdsa import SigningKey,VerifyingKey
            id_p =session['id']
            data = User.get_by_id(mysql,id_p)
            vks = VerifyingKey.from_pem(session['vk'])
            vk= format(vks.to_string().hex())
            sks = SigningKey.from_pem(session['sk'])
            sk= format(sks.to_string().hex())
            pagetype = "profil"
            # User is loggedin show them the home page
            return render_template("2profil.html", data = data, sk = sk, vk =vk, pagetype=pagetype)
        # User is not loggedin redirect to login page
    return redirect(url_for('auth.login')) 

@bp.route('/profiltab2', methods=['GET', 'POST'])
def profilku(): 
    if 'loggedin' in session:
            from ecdsa import SigningKey,VerifyingKey
            id_p =session['id']
            data = User.get_by_id(mysql,id_p)
            vks = VerifyingKey.from_pem(session['vk'])
            vk= format(vks.to_string().hex())
            sks = SigningKey.from_pem(session['sk'])
            sk= format(sks.to_string().hex())
            pagetype = "kunci"
            # User is loggedin show them the home page
            return render_template("2profil.html", data = data, sk = sk, vk =vk, pagetype=pagetype)
        # User is not loggedin redirect to login page
    return redirect(url_for('auth.login')) 

@bp.route('/profiltab3', methods=['GET', 'POST'])
def profilpw(): 
    if 'loggedin' in session:
            from ecdsa import SigningKey,VerifyingKey
            id_p =session['id']
            data = User.get_by_id(mysql,id_p)
            vks = VerifyingKey.from_pem(session['vk'])
            vk= format(vks.to_string().hex())
            sks = SigningKey.from_pem(session['sk'])
            sk= format(sks.to_string().hex())
            pagetype = "password"
            # User is loggedin show them the home page
            return render_template("2profil.html", data = data, sk = sk, vk =vk, pagetype=pagetype)
        # User is not loggedin redirect to login page
    return redirect(url_for('auth.login')) 

@bp.route('/upprofil', methods=['GET', 'POST'])
def profilbaru(): 
    if 'loggedin' in session:
        id_p =session['id']
        data = User.get_by_id(mysql,id_p)
        email           =  request.form['modmail']
        nama            =  request.form['modnama']
        foto            =  request.form['modfoto']
        bio             =  request.form['modbio']
        password        =  request.form['modps']
        kunci_privat    =  request.form['modsk']
        kunci_publik    =  request.form['modvk']
        hidemail        =  request.form['modhl']
        
        session['nama'] = nama
        session['email']  = email
        session['hml']  = hidemail
        User.update(mysql, id_p, email, nama, password, foto, bio, kunci_privat, kunci_publik, hidemail)
        return redirect(url_for('views.profil')) 
        # User is not loggedin redirect to login page
    return redirect(url_for('auth.login')) 

@bp.route('/newkey', methods=['GET', 'POST'])
def kuncibaru(): 
    if 'loggedin' in session:
        id_p =session['id']
        user = User.get_by_id(mysql, id_p)
        email           =  request.form['dmail']
        nama            =  request.form['dnama']
        foto            =  request.form['dinst']
        bio             =  request.form['dbio']
        password        =  request.form['dps']
        hidemail        =  request.form['dml']
        sk              = SigningKey.generate(curve=NIST256p)
        vk              = sk.verifying_key
        nkunci_privat    = sk.to_pem()
        nkunci_publik    = vk.to_pem()
        session['sk']   = nkunci_privat 
        session['vk']   = nkunci_publik 
        User.updateprofil(mysql, id_p, email, nama, password, foto, bio, nkunci_privat, nkunci_publik, hidemail)
        return redirect(url_for('views.profilku')) 
        # User is not loggedin redirect to login page
    return redirect(url_for('auth.login')) 

@bp.route('/newpass', methods=['GET', 'POST'])
def passbaru(): 
    if 'loggedin' in session:

        id_p =session['id']
        user = User.get_by_id(mysql, id_p)
        email           =  request.form['pmail']
        nama            =  request.form['pnama']
        foto            =  request.form['pinst']
        bio             =  request.form['pbio']
        kunci_privat    =  request.form['psk']
        kunci_publik    =  request.form['pvk']
        hidemail        =  request.form['pml']
        password        =  request.form['pass1']
        password2       =  request.form['pass2']
        if password == password2:
            User.update(mysql, id_p, email, nama, generate_password_hash(password), foto, bio, kunci_privat, kunci_publik, hidemail) 
        else:
            flash('Password Tidak Sama')
        return redirect(url_for('views.profilpw'))
        # User is not loggedin redirect to login page
    return redirect(url_for('auth.login')) 

@bp.route('/fotobaru', methods=['GET', 'POST'])
def fotobaru(): 
    if 'loggedin' in session:
        id_p =session['id']
        user = User.get_by_id(mysql, id_p)
        email           =  request.form['umail']
        nama            =  request.form['unama']
        bio             =  request.form['ubio']
        password        =  request.form['ups']
        kunci_privat    =  request.form['usk']
        kunci_publik    =  request.form['uvk']
        hidemail        =  request.form['uml']
        #nama foto
        rfoto           =  request.files['ufoto']
        nfoto           =  secure_filename(rfoto.filename)
        #UUID foto
        foto            = str(uuid.uuid1())+"_"+ nfoto
        #simpan foto ke folder
        f = request.files['ufoto']
        f.save(os.path.join(UPLOAD_FOLDER_FOTO, foto))
        session['foto'] = foto

        User.updateprofil(mysql, id_p, email, nama, password, foto, bio, kunci_privat, kunci_publik, hidemail)
        return redirect(url_for('views.profil')) 
        # User is not loggedin redirect to login page
    return redirect(url_for('auth.login')) 

@bp.route('/buat_ttd', methods=['GET', 'POST']) #Upload file pdf ke database dan folder upload
def bttd():
    if 'loggedin' in session:
        id_p = session['id']
        data = User.get_by_id(mysql,id_p)

        return render_template("3bttd.html", data = data)
    return redirect(url_for('auth.login')) 


@bp.route('/bbttd/<id_t>', methods=['GET', 'POST'])
def bbttd(id_t):
    filename = f"{id_t}.pdf"
    return send_from_directory(os.path.join('.','static','upload','file'),path=filename, as_attachment=True)

@bp.route('/nbbttd/<id_t>', methods=['GET', 'POST'])
def nbbttd(id_t):
    filename = f"{id_t}.pdf"
    return send_from_directory(os.path.join('.','static','upload','file'),path=filename, as_attachment=False)


@bp.route('/dsign', methods=['GET', 'POST'])
def dsign():
    try:
        tfile   = session['id']
        mfile   = os.path.join(UPLOAD_FOLDER_TEMP, tfile)
        os.remove(mfile)
    except Exception:
        pass
    id_p    = request.form['id_p']
    email   = request.form['email']
    nama    = request.form['nama']
    skn     = request.form['sk']
    vkr     = request.form['vk']
    vks     = VerifyingKey.from_pem(vkr)
    vkn     = format(vks.to_string().hex())
    rfile   = request.files['file']
    nfile   = secure_filename(rfile.filename)
    
    namafile1   = nfile.replace(".pdf","")
    namafile2   = secure_filename(namafile1+'_signed_by_'+nama)
    id_t        = namafile2+"_"+ str(uuid.uuid1())

    y_compensator = round(float(request.form['ycom']))
    x1 = int(request.form['x1'])
    y1 = y_compensator - int(request.form['y1'])
    x2 = int(request.form['x2'])
    y2 = y_compensator - int(request.form['y2'])
      
    region = request.form['region']
    page = request.form['page']
    data = request.files.get('file', None)

    arkan = qrgen(data.read(), page, region, x1,y1,x2,y2,id_t,email,nama,nfile,skn,vkn)
    return redirect(url_for('views.info_ttd')) 

@bp.route('/info_ttd', methods=['GET', 'POST'])
def info_ttd():
    id_p    = session['id']
    vks     = VerifyingKey.from_pem(session['vk'])
    vk      = format(vks.to_string().hex())
    id_t    = session['id_t']
    idp     = str(id_p)
    data1   = User.get_by_id(mysql,id_p)
    data2   = VTTD.get_by_id_sign(mysql,id_t)
    pth     = os.path.join(UPLOAD_FOLDER_FILE, id_t+'.pdf')
    datau   = open(pth, "rb").read()
    pth2    = os.path.join(UPLOAD_FOLDER_TEMP, idp+'.pdf')
    pth3    = UPLOAD_FOLDER_TEMP.replace("static/","")
   
    with open(pth2, 'wb') as tmp:
            tmp.write(datau)
    session['tempfile'] = pth2
    return render_template("4bttd.html", vk = vk, id_t=id_t, id_p=idp,data1=data1,data2=data2,pth=pth3)
   
    
@bp.route('/daftar_kunci', methods=['GET', 'POST'])
def dkunci():
    if 'loggedin' in session:
        id_p    = session['id']
        datak   = VDK.get_by_id_p(mysql,id_p)
        if session['id_k']  == "":
           id_k    = "" 
        else:
           id_k = session['id_k']
        data    = VDK.get_by_id_key(mysql,id_k)
        return render_template("5dkunci.html",datak=datak,id_p=id_p,data=data,id_k=id_k)
    return redirect(url_for('auth.login')) 

@bp.route('/dkunci2/<int:id_k>', methods=['GET', 'POST'])
def dkunci2(id_k):
    if 'loggedin' in session:
        session['id_k']= id_k
        return redirect(url_for('views.dkunci')) 
    return redirect(url_for('auth.login')) 


@bp.route('/dknew', methods=['GET', 'POST'])
def dknew():
    if 'loggedin' in session:
        id_p        = session['id']
        namauser    = request.form['namauser']
        kuncip      = request.form['kuncipublik']
        id_k        = ""
        VDK.create(mysql, id_k,namauser,kuncip,id_p )
        return redirect(url_for('views.dkunci')) 
    return redirect(url_for('auth.login')) 

@bp.route('/edit_kunci', methods=['GET', 'POST'])
def edit_kunci():
    if 'loggedin' in session:
        id_k        = session['id_k']
        id_p        = session['id']
        namauser    = request.form['namauser2']
        kuncip      = request.form['kuncipublik2']
        VDK.update(mysql, id_k,namauser,kuncip,id_p )
        session['id_k'] = ""
        return redirect(url_for('views.dkunci')) 
    return redirect(url_for('auth.login')) 

@bp.route('/dkunci/<int:id_k>/delete', methods=['GET', 'POST'])
def del_kunci(id_k):
    if 'loggedin' in session:
        VDK.delete(mysql, id_k)

        return redirect(url_for('views.dkunci')) 
    return redirect(url_for('auth.login')) 

@bp.route('/daftar_ttd', methods=['GET', 'POST'])
def dttd():
    if 'loggedin' in session:
        id_p =session['id']
        data_t = VTTD.get_by_id_user(mysql,id_p)

        return render_template("4dttd.html",data_t=data_t)
    return redirect(url_for('auth.login')) 


@bp.route('/verifikasi', methods=['GET', 'POST'])
def verifikasi():
    if 'loggedin' in session:
        id_p    =   session['id']
        data_k  =   VDK.get_by_id_p(mysql,id_p)
        return render_template("6vttd.html",data_k=data_k)
    return render_template("6vttd.html")

@bp.route('/hasil_verifikasi', methods=['GET', 'POST'])
def vttd2():
    #start = time.time()
    try:
        vfile   = session['vttd']
        dfile   =   os.path.join(UPLOAD_FOLDER_FILE, vfile)
        os.remove(dfile)
    except Exception:
        pass
    
    try:
        cpubkey1    =   request.form['cpubkey1']
        pkey_com    =   cpubkey1
    except: 
        cpubkey1    =   ""
        cpubkey2    =   request.form.get('cpubkey2')
        pkey_com    =   cpubkey2
    file            =   request.files['file']
    fildata1        =   file.read()
    nfile           =   secure_filename(file.filename)
    nfile0          =   nfile.replace(".pdf","_verify")
    nfile1          =   nfile0+".pdf"
    nfile2          =   os.path.join(UPLOAD_FOLDER_FILE, nfile1)
    #hashfile1       =   hashlib.sha256(fildata1)
    wkt             =   ""
    tgl             =   ""
    with open(nfile2, "wb") as fx:
        fx.write(fildata1)

    with open(nfile2, "rb") as f:
            opfile  = f.read()    

    hashfile1  = hashlib.sha256(opfile)
    hashfile2 = hashfile1.hexdigest()

    arthas          =   '1'
    lumin           =   '1'
    dayre           =   '1'
    session['vttd'] =   nfile1
    id_t            =   nfile.replace(".pdf","")


    try:
        dfile   = nfile      
        sfile   = dfile.replace(".pdf",".pdf.sig")
        uttd    = VTTD.get_by_id_sign(mysql,id_t)
        usign   = User.get_all(mysql)
        wdb     = uttd['tsign']
        wkt     = wdb.strftime("%H:%M:%S")
        tgl     = wdb.strftime("%d-%m-%Y")
        sfile1  = os.path.join(UPLOAD_FOLDER_FILE, sfile)
            
        with open(nfile2, "rb") as f:
            opfile  = f.read()
        with open(sfile1, "rb") as f:
            opsig   = f.read()
        try:
            vk = VerifyingKey.from_string(bytearray.fromhex(pkey_com), curve=NIST256p)
        except:
            flash("Format Kunci Tidak Sesuai") 
            return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,wkt=wkt,tgl=tgl,arthas=arthas,lumin=lumin,dayre=dayre)  
        try:
            vk.verify(opsig, opfile, hashlib.sha256, sigdecode=sigdecode_der)
            flash('File Asli')
        except BadSignatureError:
            flash("File Tidak Sesuai")  
        
        return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,wkt=wkt,tgl=tgl,arthas=arthas,lumin=lumin,dayre=dayre) 
    
    except:
            try:
                fhash   = VTTD.get_by_hash(mysql,hashfile2)
                fid     = fhash['id_t']
                uttd    = VTTD.get_by_id_sign(mysql,fid)    
                sfile2  = fid+".pdf.sig"
                usign   = User.get_all(mysql)
                wdb     = uttd['tsign']
                wkt     = wdb.strftime("%H:%M:%S")
                tgl     = wdb.strftime("%d-%m-%Y")
                sfile3  = os.path.join(UPLOAD_FOLDER_FILE, sfile2)
                lumin   = '2'  
                with open(nfile2, "rb") as f:
                    nopfile1  = f.read()
                with open(sfile3, "rb") as f:
                    nopsig1   = f.read()
                try:
                    vk = VerifyingKey.from_string(bytearray.fromhex(pkey_com), curve=NIST256p)
                except:
                    flash("Wrong Key Format") 
                    return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,wkt=wkt,tgl=tgl,arthas=arthas,lumin=lumin,dayre=dayre)  

                try:
                    vk.verify(nopsig1, nopfile1, hashlib.sha256, sigdecode=sigdecode_der)
                    flash('File Asli','success')
                except BadSignatureError:
                    flash("File Tidak Sesuai", 'danger')  

                return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,wkt=wkt,tgl=tgl,arthas=arthas,lumin=lumin,dayre=dayre) 
    
            except:
                try:
                    dfile   = nfile      
                    sfile   = dfile.replace(".pdf",".pdf.sig")
                    uttd    = STTD.get_by_id_sign(mysql,id_t)
                    usign   = User.get_all(mysql)
                    try:
                        dfile1  = os.path.join(UPLOAD_FOLDER_FILE, dfile)
                        sfile1  = os.path.join(UPLOAD_FOLDER_FILE, sfile)
                        
                        with open(nfile2, "rb") as f:
                            mopfile1  = f.read()
                        with open(sfile1, "rb") as f:
                            mopsig1   = f.read()
                        dayre   = '2'
                        lumin   = '1' 
                        arthas  = '1'   
                        try:
                            vk = VerifyingKey.from_string(bytearray.fromhex(pkey_com), curve=NIST256p)
                        except:
                            flash("Format Kunci Salah") 
                            return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,arthas=arthas,lumin=lumin,dayre=dayre)  

                        try:
                            vk.verify(mopsig1, mopfile1, hashlib.sha256, sigdecode=sigdecode_der)
                            flash('File Asli','success')
                        except BadSignatureError:
                            flash("File Tidak Sesuai", 'danger')  

                        return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,arthas=arthas,lumin=lumin,dayre=dayre)
                    except:
                        try:
                            fhash   = STTD.get_by_hash(mysql,hashfile2)
                            fid     = fhash['mid']
                            uttd    = STTD.get_by_id_sign(mysql,fid)    
                            sfile2  = fid+".pdf.sig"
                            usign   = User.get_all(mysql)
                            sfile3  = os.path.join(UPLOAD_FOLDER_FILE, sfile2)
                            dayre   = '2'
                            arthas  = '1' 
                            lumin   = '2'  
                            with open(nfile2, "rb") as f:
                                mopfile2  = f.read()
                            with open(sfile3, "rb") as f:
                                mopsig2   = f.read()
                            try:
                                vk = VerifyingKey.from_string(bytearray.fromhex(pkey_com), curve=NIST256p)
                            except:
                                flash("Format Kunci Salah") 
                                return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,arthas=arthas,lumin=lumin,dayre=dayre)  

                            try:
                                vk.verify(mopsig2, mopfile2, hashlib.sha256, sigdecode=sigdecode_der)
                                flash('File Asli','success')
                            except BadSignatureError:
                                flash("File Tidak Sesuai", 'danger')  

                            return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,arthas=arthas,lumin=lumin,dayre=dayre)
                        except:
                            arthas = '2'
                            dayre  = '1'
                            flash("File Tidak Ditemukan") 
                            return render_template("7vttd.html",id_t=id_t,nfile=nfile1,arthas=arthas,lumin=lumin,dayre=dayre) 
                except:
                    arthas = '2'
                    dayre  = '1'
                    flash("File Tidak Ditemukan") 
                    return render_template("7vttd.html",id_t=id_t,nfile=nfile1,arthas=arthas,dayre=dayre,lumin=lumin)               

               
@bp.route('/chprofil/<int:id_other>', methods=['GET', 'POST'])
def vttd3(id_other): 
    session['other'] = id_other
    return redirect(url_for('views.pengguna')) 

# Verifikasi dari kode QR

@bp.route('/qread/<id_t>', methods=['GET', 'POST'])
def qread(id_t):
    session['qsign'] = id_t
    return redirect(url_for('views.qvttd')) 

@bp.route('/qvttd', methods=['GET', 'POST'])
def qvttd():
    id_t    =   session['qsign']
    nfile   =   str(id_t)+'.pdf'
    arthas  =   '1'
    try:
        dfile   = nfile      
        try:
            dfile1  = os.path.join(UPLOAD_FOLDER_FILE, dfile)
            with open(dfile1, "rb") as f:
                opfile = f.read()
        except:
            arthas = '2'
    except:
        arthas = '2'    
    if 'loggedin' in session:
        id_p    =   session['id']
        data_k  =   VDK.get_by_id_p(mysql,id_p)
        return render_template("8vttd.html",data_k=data_k,id_t=id_t,arthas=arthas)
    return render_template("8vttd.html",id_t=id_t,arthas=arthas)

#QR Verification
@bp.route('/verifikasi_qr', methods=['GET', 'POST'])
def qvery():
    try:
        cpubkey1    =   request.form['cpubkey1']
        pkey_com    =   cpubkey1
    except: 
        cpubkey1    =   ""
        cpubkey2    =   request.form.get('cpubkey2')
        pkey_com    =   cpubkey2

    nfile           =   session['qsign']
    nfile1          =   nfile+".pdf"
    nfile2          =   os.path.join(UPLOAD_FOLDER_FILE, nfile1)
    arthas          =   '1'
    session['vttd'] =   nfile1
    id_t            =   nfile
    #----------------------------
    #hashfile1       =   hashlib.sha256(fildata1)
    wkt             =   ""
    tgl             =   ""

    with open(nfile2, "rb") as f:
            opfile  = f.read()    

    hashfile1  = hashlib.sha256(opfile)
    hashfile2 = hashfile1.hexdigest()

    arthas          =   '1'
    lumin           =   '1'
    dayre           =   '1'
    session['vttd'] =   nfile1
    id_t            =   nfile.replace(".pdf","")

     
    try:
        dfile   = nfile      
        sfile   = dfile.replace(".pdf",".pdf.sig")
        uttd    = VTTD.get_by_id_sign(mysql,id_t)
        usign   = User.get_all(mysql)
        wdb     = uttd['tsign']
        wkt     = wdb.strftime("%H:%M:%S")
        tgl     = wdb.strftime("%d-%m-%Y")
        sfile1  = os.path.join(UPLOAD_FOLDER_FILE, sfile)
        
        dfile1  = os.path.join(UPLOAD_FOLDER_FILE, dfile)
        sfile1  = os.path.join(UPLOAD_FOLDER_FILE, sfile)
        with open(dfile1, "rb") as f:
            opfile = f.read()
        with open(sfile1, "rb") as f:
            opsig = f.read()
        try:
            vk = VerifyingKey.from_string(bytearray.fromhex(pkey_com), curve=NIST256p)
        except:
            flash("Format Kunci Tidak Sesuai") 
            return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,wkt=wkt,tgl=tgl,arthas=arthas,lumin=lumin,dayre=dayre)  
        try:
            vk.verify(opsig, opfile, hashlib.sha256, sigdecode=sigdecode_der)
            flash('File Asli')
        except BadSignatureError:
            flash("File Tidak Sesuai")  
        
        return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,wkt=wkt,tgl=tgl,arthas=arthas,lumin=lumin,dayre=dayre) 
    
    except:
            try:
                fhash   = VTTD.get_by_hash(mysql,hashfile2)
                fid     = fhash['id_t']
                uttd    = VTTD.get_by_id_sign(mysql,fid)    
                sfile2  = fid+".pdf.sig"
                usign   = User.get_all(mysql)
                wdb     = uttd['tsign']
                wkt     = wdb.strftime("%H:%M:%S")
                tgl     = wdb.strftime("%d-%m-%Y")
                sfile3  = os.path.join(UPLOAD_FOLDER_FILE, sfile2)

                with open(nfile2, "rb") as f:
                    nopfile1  = f.read()
                with open(sfile3, "rb") as f:
                    nopsig1   = f.read()
                try:
                    vk = VerifyingKey.from_string(bytearray.fromhex(pkey_com), curve=NIST256p)
                except:
                    flash("Wrong Key Format") 
                    return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,wkt=wkt,tgl=tgl,arthas=arthas,lumin=lumin,dayre=dayre)  

                try:
                    vk.verify(nopsig1, nopfile1, hashlib.sha256, sigdecode=sigdecode_der)
                    flash('File Asli','success')
                except BadSignatureError:
                    flash("File Tidak Sesuai", 'danger')  

                return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,wkt=wkt,tgl=tgl,arthas=arthas,lumin=lumin,dayre=dayre) 
    
            except:
                try:
                    dfile   = nfile      
                    sfile   = dfile.replace(".pdf",".pdf.sig")
                    uttd    = STTD.get_by_id_sign(mysql,id_t)
                    usign   = User.get_all(mysql)
                    try:
                        dfile1  = os.path.join(UPLOAD_FOLDER_FILE, dfile)
                        sfile1  = os.path.join(UPLOAD_FOLDER_FILE, sfile)
                        
                        with open(nfile2, "rb") as f:
                            mopfile1  = f.read()
                        with open(sfile1, "rb") as f:
                            mopsig1   = f.read()
                        dayre   = '2'
                        lumin   = '1' 
                        arthas  = '1'   
                        try:
                            vk = VerifyingKey.from_string(bytearray.fromhex(pkey_com), curve=NIST256p)
                        except:
                            flash("Format Kunci Salah") 
                            return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,arthas=arthas,lumin=lumin,dayre=dayre)  

                        try:
                            vk.verify(mopsig1, mopfile1, hashlib.sha256, sigdecode=sigdecode_der)
                            flash('File Asli','success')
                        except BadSignatureError:
                            flash("File Tidak Sesuai", 'danger')  

                        return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,arthas=arthas,lumin=lumin,dayre=dayre)
                    except:
                        try:
                            fhash   = STTD.get_by_hash(mysql,hashfile2)
                            fid     = fhash['mid']
                            uttd    = STTD.get_by_id_sign(mysql,fid)    
                            sfile2  = fid+".pdf.sig"
                            usign   = User.get_all(mysql)
                            sfile3  = os.path.join(UPLOAD_FOLDER_FILE, sfile2)
                            dayre   = '2'
                            arthas  = '1' 

                            with open(nfile2, "rb") as f:
                                mopfile2  = f.read()
                            with open(sfile3, "rb") as f:
                                mopsig2   = f.read()
                            try:
                                vk = VerifyingKey.from_string(bytearray.fromhex(pkey_com), curve=NIST256p)
                            except:
                                flash("Format Kunci Salah") 
                                return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,arthas=arthas,lumin=lumin,dayre=dayre)  

                            try:
                                vk.verify(mopsig2, mopfile2, hashlib.sha256, sigdecode=sigdecode_der)
                                flash('File Asli','success')
                            except BadSignatureError:
                                flash("File Tidak Sesuai", 'danger')  

                            return render_template("7vttd.html",id_t=id_t,uttd=uttd,usign=usign,nfile=nfile1,arthas=arthas,lumin=lumin,dayre=dayre)
                        except:
                            arthas = '2'
                            dayre  = '1'
                            flash("File Tidak Ditemukan") 
                            return render_template("7vttd.html",id_t=id_t,nfile=nfile1,arthas=arthas,lumin=lumin,dayre=dayre) 
                except:
                    arthas = '2'
                    dayre  = '1'
                    flash("File Tidak Ditemukan") 
                    return render_template("7vttd.html",id_t=id_t,nfile=nfile1,arthas=arthas,dayre=dayre,lumin=lumin)               

               


#ERROR Handler----------------------------------------------------------------------------
@bp.errorhandler(403)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('403.html'), 403

#Multi User Signature--------------------------------------------------------------------------------------
@bp.route('/multi_signature', methods=['GET', 'POST']) #Upload file pdf ke database dan folder upload
def ssttd():
    if 'loggedin' in session:
        uid     = session['id']
        data    = User.get_by_id(mysql,uid)
        return render_template("9bttd.html", data = data)
    return redirect(url_for('auth.login')) 

@bp.route('/msign', methods=['GET', 'POST'])
def msign():
    try:
        tfile   = session['id']
        mfile   = os.path.join(UPLOAD_FOLDER_TEMP, tfile)
        os.remove(mfile)
    except Exception:
        pass
    id_p    = request.form['id_p']
    email   = request.form['email']
    nama    = request.form['nama']
    #one creation key--------------------------------
    skna    = SigningKey.generate(curve=NIST256p)
    vkna    = skna.verifying_key
    sk      = skna.to_pem()
    vk      = vkna.to_pem()
    skr     = SigningKey.from_pem(sk)
    vkr     = VerifyingKey.from_pem(vk)
    vkn     = format(vkr.to_string().hex())
    skc     = format(skr.to_string().hex())
    skn     = sk.decode("utf-8")

    #--------------------------------------------
    rfile   = request.files['file']
    nfile   = secure_filename(rfile.filename)
    namafile1   = nfile.replace(".pdf","")
    namafile2   = secure_filename(namafile1+'_signed_by_'+nama)
    id_t        = namafile2+"_"+ str(uuid.uuid1())
    nsig        = request.form['nsig']
    nsed        = 0
    y_compensator = round(float(request.form['ycom']))
    x1 = int(request.form['x1'])
    y1 = y_compensator - int(request.form['y1'])
    x2 = int(request.form['x2'])
    y2 = y_compensator - int(request.form['y2'])
      
    region = request.form['region']
    page = request.form['page']
    data = request.files.get('file', None)

    arkan = mgen(data.read(), page, region, x1,y1,x2,y2,id_t,email,nama,nfile,skn,vkn,nsed,nsig,skc)
    return redirect(url_for('views.isttd')) 

@bp.route('/multi_info', methods=['GET', 'POST'])
def isttd():
    id_p    = session['id']
    mid     = session['mid']
    fid     = STTD.get_by_id_sign(mysql,mid)
    vk      = fid['pkey']
    sk      = fid['skey']
    pth     = os.path.join(UPLOAD_FOLDER_FILE, mid+'.pdf')
    idp     = str(id_p)
    datau   = open(pth, "rb").read()
    pth2    = os.path.join(UPLOAD_FOLDER_TEMP, idp+'.pdf')
    pth3    = UPLOAD_FOLDER_TEMP.replace("static/","")  
    with open(pth2, 'wb') as tmp:
            tmp.write(datau)
    session['tempfile'] = pth2
    return render_template("9ittd.html", vk = vk, sk = sk, id_t=mid, id_p=idp, fid=fid, pth=pth3)    

    

@bp.route('/multi_list', methods=['GET', 'POST'])
def lsttd():
    if 'loggedin' in session:
        id_p =session['id']
        data_1 = STTD.get_by_id1(mysql,id_p)
        data_2 = STTD.get_by_id2(mysql,id_p)
        data_3 = STTD.get_by_id3(mysql,id_p)
        data_4 = STTD.get_by_id4(mysql,id_p)
        return render_template("9dttd.html",data_1=data_1,data_2=data_2,data_3=data_3,data_4=data_4)
    return redirect(url_for('auth.login')) 

@bp.route('/co_signature', methods=['GET', 'POST']) #Upload file pdf ke database dan folder upload
def cosign():
    if 'loggedin' in session:
        uid     = session['id']
        data    = User.get_by_id(mysql,uid)
        return render_template("10cosign.html", data = data)
    return redirect(url_for('auth.login')) 

@bp.route('/ch_prikey', methods=['GET', 'POST']) #Upload file pdf ke database dan folder upload
def chkey():
    if 'loggedin' in session:
        uid     = session['id']
        data    = User.get_by_id(mysql,uid)
        return render_template("10cosign.html", data = data)
    return redirect(url_for('auth.login')) 

#CoSign--------------------------------
@bp.route('/csign', methods=['GET', 'POST'])
def csign():
        try:
            tfile   = session['id']
            mfile   = os.path.join(UPLOAD_FOLDER_TEMP, tfile)
            os.remove(mfile)
        except Exception:
            pass
        id_p    = request.form['id_p']
        email   = request.form['email']
        prikey  = request.form['prikey']
        file            =   request.files['file']
        fildata1        =   file.read()
        nfile           =   secure_filename(file.filename)
        nfile0          =   nfile.replace(".pdf","_check")
        nfile1          =   nfile0+".pdf"
        nfile2          =   os.path.join(UPLOAD_FOLDER_FILE, nfile1)
        nfile3          =   nfile.replace(".pdf","")
        with open(nfile2, "wb") as fx:
                    fx.write(fildata1)
        with open(nfile2, "rb") as f:
                    opfile  = f.read()    

        hashfile1  = hashlib.sha256(opfile)
        hashfile2 = hashfile1.hexdigest()

        arthas          =   '1'
        lumin           =   '1'
 #   try:
        try:
            uttd    = STTD.get_by_id_sign(mysql,nfile3)
            mid     = uttd['mid']
        except:
            fhash   = STTD.get_by_hash(mysql,hashfile2)
            mid     = fhash['mid']
            uttd    = STTD.get_by_id_sign(mysql,mid) 
            mid     = uttd['mid']   
        skn     = uttd['sigkey']
        sdb     = uttd['skey']
        skc     = sdb
        pdb     = uttd['pkey']
        vkn     = pdb
        nfile   = uttd['filename']
        id_t    = uttd['mid']
        nsig    = uttd['nsig']
        nsed    = uttd['nsed']
        dbfile1 = os.path.join(UPLOAD_FOLDER_FILE, mid+".pdf")
        with open(dbfile1, "rb") as f:
            dbfile2  = f.read() 
        if  prikey != sdb:
            arthas = 2
            if sdb == "Proses Selesai":
                flash("Proses Tanda Tangan Selesai")
            else: 
                flash("Kunci Privat Salah")
            return render_template("10ittd.html",id_t=mid,nfile=nfile,vk=pdb,sk=sdb,lumin=lumin,arthas=arthas) 
        else:
            if uttd['nsed'] == uttd['nsig']:
                flash("Proses Tanda Tangan Selesai") 
                return render_template("10ittd.html",id_t=mid,nfile=nfile,vk=pdb,sk=sdb,lumin=lumin,arthas=arthas) 

            y_compensator = round(float(request.form['ycom']))
            x1 = int(request.form['x1'])
            y1 = y_compensator - int(request.form['y1'])
            x2 = int(request.form['x2'])
            y2 = y_compensator - int(request.form['y2'])
            
            region = request.form['region']
            page = request.form['page']
            os.remove(nfile2)
            arkan = cgen(dbfile2, page, region, x1,y1,x2,y2,id_t,email,id_p,nfile,skn,vkn,nsed,nsig,skc)
    #--------------------------------------------
 #   except:
 #       arthas = '2'
 #       flash("File Not Found") 
 #       return render_template("10ittd.html",arthas=arthas,lumin=lumin) 


        return redirect(url_for('views.cisttd')) 

@bp.route('/co_info', methods=['GET', 'POST'])
def cisttd():
    id_p    = session['id']
    arthas  = "1"
    mid1    = session['mid']
    fid     = STTD.get_by_id_sign(mysql,mid1)
    mid     = fid['mid']
    vk      = fid['pkey']
    sk      = fid['skey']
    session.pop('mid1', None)
    idp     = str(id_p)
    pth     = os.path.join(UPLOAD_FOLDER_FILE, mid+'.pdf')
    datau   = open(pth, "rb").read()
    pth2    = os.path.join(UPLOAD_FOLDER_TEMP, idp+'.pdf')
    pth3    = UPLOAD_FOLDER_TEMP.replace("static/","")  
    with open(pth2, 'wb') as tmp:
            tmp.write(datau)
    session['tempfile'] = pth2

    return render_template("10ittd.html", vk = vk, sk = sk,  id_t=mid, id_p=idp, fid=fid, pth=pth3, arthas=arthas)  