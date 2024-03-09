from flask_mysqldb import MySQL  

mysql = MySQL()

def init_db(app):    
    # Domainesia
    #app.config['MYSQL_HOST'] = 'localhost'
    #app.config['MYSQL_USER'] = 'qsignxyz_adityara'
    #app.config['MYSQL_PASSWORD'] = 'axaxa'
    #app.config['MYSQL_DB'] = 'qsignxyz_db_qsign'
    #app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    # Localhost
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'db_qsign'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql = MySQL(app)

    with app.app_context():
        cursor = mysql.connection.cursor()

        # Create tabel pengguna
        cursor.execute('''CREATE TABLE IF NOT EXISTS tb_pengguna (
            id_p INT(11) NOT NULL,
            email VARCHAR(64) NOT NULL,
            nama VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            foto TEXT NOT NULL,
            bio TEXT NULL,
            kunci_privat TEXT NULL,
            kunci_publik TEXT NULL,
            hidemail int(1) NULL,
            PRIMARY KEY (id_p)            
        )''')

       
        # Create tabel tanda tangan
        cursor.execute('''CREATE TABLE IF NOT EXISTS tb_ttd (
            id_t INT(11) NOT NULL AUTO_INCREMENT,
            namafile VARCHAR(255) NOT NULL,
            hvalue TEXT NOT NULL,
            pkey TEXT NOT NULL,
            tsign TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            id_p INT(11) NOT NULL,
            PRIMARY KEY (id_t)            
        )''')  

       # creaete tabel multi ttd
        cursor.execute('''CREATE TABLE IF NOT EXISTS tb_sttd (
            mid VARCHAR(256) NOT NULL, 
            filename VARCHAR(256) NOT NULL, 
            hvalue TEXT NOT NULL, 
            sigkey TEXT NOT NULL, 
            skey TEXT NOT NULL, 
            pkey TEXT NOT NULL, 
            nsig INT(11) NOT NULL, 
            nsed INT(11) NOT NULL, 
            uid1 INT(11) NULL, 
            tsig1 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL, 
            uid2 INT(11) NULL, 
            tsig2 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL, 
            uid3 INT(11) NULL, 
            tsig3 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL, 
            uid4 INT(11) NULL, 
            tsig4 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
            PRIMARY KEY (mid)
        )''') 
        
        # Create tabel daftar kunci
        cursor.execute('''CREATE TABLE IF NOT EXISTS tb_dk (
            id_k INT(11) AUTO_INCREMENT,
            nama VARCHAR(255) NOT NULL,
            k_publik VARCHAR(255) NOT NULL,
            id_p INT(11) NOT NULL,
            PRIMARY KEY (id_k)            
        )''')

        # commit to DB
        mysql.connection.commit()

        # close connection
        cursor.close()

    return mysql