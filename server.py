from fastapi import FastAPI
from datetime import datetime, timedelta

import server_db

app = FastAPI()


@app.post("/system_id")
def hello(data: dict):
    name = data.get("name")
    system_id = name[1:]
    if name[0] == '#':
        if server_db.find_users(system_id) and check_time(system_id):
            return {"message": "Yes"}
        else:
            server_db.delete_user(system_id)
            return {"message": "No"}
    else:
        if check_key(name):
            return {"message": f"True"}
        else:
            return {"message": "False"}


@app.post("/time")
def hello(data: dict):
    name = data.get("system_id")
    time_left = license_time(name)
    return {"message": f'{time_left.days}'}


def check_key(key_sysid):
    key, sys_id = key_sysid.split('#')
    date = license_time_unix(server_db.find_license_time())
    if server_db.find_keys(key):
        server_db.delete_key(key)
        server_db.add_user_data(sys_id, key, date)
        return True
    else:
        return False


def license_time_unix(license_time):
    print(license_time)
    time = datetime.now()
    license_end = time + timedelta(days=license_time)
    unix_time = int(license_end.timestamp())
    return unix_time


def check_time(sys_id):
    time = datetime.now()
    license_end_time = datetime.fromtimestamp(int(server_db.find_time(sys_id)))
    time_now = datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
    time_now = datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
    if time_now > license_end_time:
        return False
    else:
        return True


def license_time(sys_id):
    time = datetime.now()
    license_end_time = datetime.fromtimestamp(int(server_db.find_time(sys_id)))
    time_now = datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
    time_now = datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
    left_days = license_end_time - time_now
    return left_days