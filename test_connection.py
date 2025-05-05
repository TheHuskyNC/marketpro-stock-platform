from db_connect import get_db_connection

db = get_db_connection()
print("Connected to MySQL Database Successfully!")
db.close()