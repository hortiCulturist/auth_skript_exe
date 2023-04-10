import sqlite3 as sqlt

db_name = 'user_database.db'


def start_db():
    base = sqlt.connect(db_name)
    base.execute('CREATE TABLE IF NOT EXISTS "User" ("id"	INTEGER NOT NULL UNIQUE,'
                 '"computer_serial_number"     BLOB,'
                 '"key"                        BLOB,'
                 '"expiration_date"            INTEGER,'
                 'PRIMARY KEY("id" AUTOINCREMENT))')
    base.execute('CREATE TABLE IF NOT EXISTS "Key" ("id"	INTEGER NOT NULL UNIQUE,'
                 '"key"            BLOB,'
                 'PRIMARY KEY("id" AUTOINCREMENT))')
    base.execute('CREATE TABLE IF NOT EXISTS "License_time" ('
                 '"time"	INTEGER);')
    base.commit()


start_db()


def add_key(key):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('INSERT INTO Key VALUES (null, ?)', (key,))
    return data


def add_user_data(computer_serial_number, key, expiration_date):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('INSERT INTO User VALUES (null, ?, ?, ?)', (computer_serial_number,
                                                                       key,
                                                                       expiration_date))
    return data


def find_keys(key):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        all_data = cur.execute('SELECT * FROM Key where key = ?', (key,)).fetchone()
    try:
        if key in all_data:
            return True
        else:
            return False
    except TypeError:
        return False


def all_keys():
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        all_data = cur.execute('SELECT * FROM Key').fetchall()
        return all_data


def find_users(system_id):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        all_data = cur.execute('SELECT * FROM User where computer_serial_number = ?', (system_id,)).fetchone()
        try:
            if system_id in all_data:
                return True
            else:
                return False
        except TypeError:
            return False


def find_time(system_id):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        all_data = cur.execute('SELECT expiration_date FROM User where computer_serial_number = ?',
                               (system_id,)).fetchone()
        return all_data[0]


def add_license_time(lic_time):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT * FROM License_time').fetchone()
        if data is None:
            cur.execute('INSERT INTO License_time VALUES (?)', (lic_time,))
        else:
            cur.execute('UPDATE License_time SET time = ?', (lic_time,))
        return data


def find_license_time():
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        all_data = cur.execute('SELECT * FROM License_time').fetchone()
        return all_data[0]


def delete_key(key):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM Key WHERE key = ?', (key,))
    return True


def delete_user(system_id):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        if find_users(system_id):
            cur.execute('DELETE FROM User WHERE computer_serial_number = ?', (system_id,))
            return True
        return False
