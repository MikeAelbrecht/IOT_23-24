import mysql.connector
import datetime

database = mysql.connector.connect(
    host="localhost",
    user="iot",
    password="iot",
    database="iot"
)

cursor = database.cursor()

query = "INSERT INTO waarden (datum, tijd) VALUES (%s, %s)"
values = (datetime.datetime.now().date(), datetime.datetime.now().time())

cursor.execute(query, values)

database.commit()
