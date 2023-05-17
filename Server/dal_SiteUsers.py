import sqlite3
import hashlib


# Creating the Data Base
def connect_db():
    db = sqlite3.connect('database_SiteUsers.db')
    db.cursor().execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    db.commit()
    return db

# Receiving sql command
# Executing changes in the DB
def db_change(connection,sql):
    cursor = connection.cursor()
    cursor.execute(sql) # execute the SQl command
    connection.commit() #DO the command
    print( "SQL executed succesfully")

# Returning the result of the query
def db_query(connection,sql, params = ''):
    cursor = connection.cursor()
    if  params != '':
        cursor.execute(sql,params)
    else:
        cursor.execute(sql)
    rows = cursor.fetchall()
    # print(rows)
    return rows


# Checking if data received (user,password) is in the DB
def in_DB(connection, user, passw):
    sql = f"SELECT * FROM users where password= '{passw}' and username = '{user}' "
    rows = db_query(connection, sql)
    if len(rows) != 0:
            return True
    return False

# Checking if data received (user,password) is in the DB
def in_DB_protected(connection, user, passw):
    sql = f"SELECT * FROM users where password= ? and username = ? "
    rows = db_query(connection, sql, (passw,user))
    if len(rows) != 0:
            return True
    return False

# Encrypting the user's password
def hash_to_pass(passw):
    hash_md5 = hashlib.md5(passw.encode())  # make hash MD5 to  string
    hash_passw = hash_md5.hexdigest()
    return hash_passw

# Adding users to the data base after clearing it
def Add_users_to_DB():
    connection = connect_db()
    sql_delete = """DELETE FROM users;"""
    db_change(connection,sql_delete)
    sql = f"""INSERT INTO users VALUES ("admin",'{hash_to_pass("admin")}');"""
    db_change(connection,sql)
    sql = f"""INSERT INTO users VALUES ("user1",'{hash_to_pass("pass1")}');"""
    db_change(connection,sql)