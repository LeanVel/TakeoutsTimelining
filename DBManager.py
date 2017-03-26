import sqlite3

def initDB(dbName):

    #connector global variable
    global conn

    #cursor global varaible
    global cursor

    try:

        # establish connection with the DB
        conn = sqlite3.connect(dbName)
        # conn = sqlite3.connect(":memory:")

        # get cursor to manipulate the DB
        cursor = conn.cursor()

        # create a table (if it doesn't exist)
        cursor.execute("""create table if not exists timeline
                      (timeStamp text, sourceType text,
                       data text) """)

    except sqlite3.Error as e:
        print("Error %s:" % e.args[0])

def insertSingleRecord(data) :

    # insert data, where data is a tuple ('timeStamp', 'sourceType', 'data')

    # data should look like ('1488885118000', 'LocationHistory', 'latitudeE7 : 490737983, longitudeE7 : 174213983, accuracy : 20, altitude : 182'),

    cursor.executemany("INSERT INTO timeline VALUES (?,?,?)", data )

    # save data to database
    conn.commit()

def insertMultipleRecords(data):

    try:
        # insert data, where data is a list of tuples [('timeStamp', 'sourceType', 'data')]
        cursor.executemany("INSERT INTO timeline VALUES (?,?,?)", data)

        # save data to database
        conn.commit()

    except sqlite3.Error as e:
        print("Error %s:" % e.args[0])


def printTable():

    for row in cursor.execute("SELECT * FROM timeline ORDER BY timeStamp DESC "):
        print(row)