from flask import Flask, render_template, request, redirect, url_for, flash,Blueprint, flash, g, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
# import modules
import qrcode
from PIL import Image
# taking image which user wants
# in the QR code center
#for the app
from flask import Flask, render_template, request, send_file 
import os
import tempfile
import datetime
from datetime import datetime as datetm
#for logging
import traceback
import sys 
import hashlib
import time
#utils for the digital signature (keys / certificates)
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization import pkcs12

#utils for pdf signing / manipulation
from endesive.pdf import cms
from PIL import Image, ImageOps
from core.viewsm import VTTD
from werkzeug.utils import secure_filename
from core.extension import mysql
from ecdsa import SigningKey
from ecdsa.util import sigencode_der, sigdecode_der
import uuid as uuid

bp = Blueprint('qsign', __name__)

QR = "static/images"
UPLOAD_FOLDER_FILE = "static/upload/file"
@bp.route('/qrgen', methods=['GET', 'POST'])
def qrgen(docdata, page, region, x1,y1,x2,y2,id_t,email,nama,nfile,skn,vkn):
  #  start = time.time()
    id_p =session['id']
    Logo_link = 'static/assets/img/stamp/icon.png'
   # icon_img = os.path.join(Logo_link, "icon.png")

    logo = Image.open(Logo_link)

    # taking base width
    basewidth = 100

    # adjust image size
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    
    logo = logo.resize((basewidth, hsize))
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=2
    )

     # HOSTING
    #url = 'http://qsign.xyz/qread/'+id_t
    
    # LOCALHOST
    url = 'http://127.0.0.1:5000/qread/'+id_t

    # adding URL or text to QRcode
    QRcode.add_data(url)

    # generating QR code
    QRcode.make()

    # taking color name from user
    QRcolor = 'blue'

    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    
    old_im = QRimg
    old_size = old_im.size
    new_size = (QRimg.size[0]+20, QRimg.size[1]+20)

    new_im = Image.new("RGB", new_size)   ## luckily, this is already black!
    box = tuple((n - o) // 2 for n, o in zip(new_size, old_size))
    new_im.paste(old_im, box)

    # save the QR code generated
    nqr = str(id_p)
    new_im.save(os.path.join(QR, nqr+'.jpg'))

    # Masukan QR ke PDF
    qr_link = 'static/images/'
    qr_img = os.path.join(qr_link, nqr+'.jpg')

    res = Image.open(qr_img)
    _fr,fname = tempfile.mkstemp(".pdf")
    #fname =" b.pdf"
    
    one_day = datetime.timedelta(1, 0, 0)
    private_key = rsa.generate_private_key(
      public_exponent=65537,
      key_size=2048,
      backend=default_backend()
    )
    public_key = private_key.public_key()
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([
      x509.NameAttribute(NameOID.COMMON_NAME, nama),
    ]))
    builder = builder.issuer_name(x509.Name([
      x509.NameAttribute(NameOID.COMMON_NAME, u'Qsign'),
    ]))
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 365))
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.public_key(public_key)
    builder = builder.add_extension(
      x509.SubjectAlternativeName(
          [x509.DNSName("@Qsign")]
      ),
      critical=False
    )
    builder = builder.add_extension(
      x509.BasicConstraints(ca=False, path_length=None), critical=True,
    )
    certificate = builder.sign(
      private_key=private_key, algorithm=hashes.SHA256(),
      backend=default_backend()
    )
    p12 = pkcs12.serialize_key_and_certificates(b'test', private_key, certificate, [certificate], serialization.BestAvailableEncryption(b'1234'))
    y = pkcs12.load_key_and_certificates(p12, b'1234', default_backend())

    dtn = datetm.now()
    date = dtn.strftime("%d/%m/%Y %H:%M:%S")
    tspurl = "http://public-qlts.certum.pl/qts-17"
    dct = {
        "aligned": 0,
        "sigflags": 1,
        "sigflagsft": 132,
        "sigpage": int(page)-1,
        "sigbutton": True,
        "sigfield": "Signature",
        "sigandcertify": True,
        "signaturebox": (max(x1,x2),(max(y1,y2)),min(x1,x2),min(y1,y2)), 
        "signature_img": res,
        "contact": email,
        "location": region,
        "signingdate": date,
        "reason": "To execute/formalize/affirm the contract", 
        "password": "1234",
    }

    with open(fname, 'wb') as fx: 
      fx.write(docdata)

    datau = open(fname, "rb").read()
   
    datas = cms.sign(datau, dct, y[0], y[1], y[2], "sha256", timestampurl=tspurl)

    namafile0 = id_t+'.pdf'
    namafile1 = secure_filename(namafile0)
    namafile2 = os.path.join(UPLOAD_FOLDER_FILE, namafile1)

    namafile3 = nfile.replace(".pdf","")
    namafile4 = namafile3+'_signed_by_'+nama
    namafile5 = secure_filename(namafile4)+".pdf"
    #namafile6 = os.path.join(UPLOAD_FOLDER_FILE, namafile5)
   #fp.save(os.path.join(UPLOAD_FOLDER_FILE, fname))     
    signature =""
    tsign = datetm.now()
    
    with open(namafile2, "wb") as fp:
      fp.write(datau)
      fp.write(datas)

    sks   = SigningKey.from_pem(skn, hashlib.sha256)

    with open(namafile2, "rb") as fp:
      tbs = fp.read()
    
    qsig = sks.sign_deterministic(tbs, sigencode=sigencode_der)
    datafile = namafile2+".sig"
    #with open(namafile6, "wb") as fp:
    #  fp.write(qsig)
    with open(datafile, "wb") as f:
      f.write(qsig)
     
  # end = time.time()
   # timecek   = ((end - start)*1000)
    hashfile1  = hashlib.sha256(tbs)
    hashfile2 = hashfile1.hexdigest()
    wat     = "signer"
    ttdx       = int.from_bytes(qsig, byteorder='big')
    VTTD.create(mysql, id_t, namafile5,hashfile2, vkn, tsign, id_p)
    #VTTD.timeto(mysql, id_t, hashfile2, ttdx, timecek,wat)
    os.close(_fr) 
    session['id_t'] = id_t
    return id_t