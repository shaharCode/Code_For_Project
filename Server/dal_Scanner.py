
import sqlite3

# Creating the Data Base
def connect_db():
    db = sqlite3.connect('database_Scanner.db')
    db.cursor().execute("CREATE TABLE IF NOT EXISTS Log (date TEXT, attack_type TEXT, result TEXT, siteIP TEXT)")
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
def db_query(connection,sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# deletes all data in order to have a clean data base at the start
def clean_db(connection):
    sql_delete = """DELETE FROM Log;"""
    db_change(connection,sql_delete)

