import sqlite3

# Creating the Data Base
def connect_db():
    db = sqlite3.connect('database_SiteData.db')
    db.cursor().execute("CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, comment TEXT)")
    db.commit()
    return db

# Adding data received (comment) to the DB
def add_comment(connection, comment):
    print(comment)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO comments (comment) '
                        'VALUES (?)', (comment,))
    connection.commit()


# Returning the comments in the DB
def get_comments(connection, search_query=None):
    results = []
    get_all_query = 'SELECT comment FROM comments'
    for (comment,) in connection.cursor().execute(get_all_query).fetchall():
        if search_query is None or search_query in comment:
            results.append(comment)
    return results


# Receiving sql command
# Executing changes in the DB
def db_change(connection,sql):
    cursor = connection.cursor()
    cursor.execute(sql) # execute the SQl command
    connection.commit() #DO the command
    print( "SQL executed succesfully")


# deletes all data in order to have a clean data base at the start
def clean_db(connection):
    sql_delete = """DELETE FROM comments;"""
    db_change(connection,sql_delete)
