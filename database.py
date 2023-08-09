# import mysql.connector 

# def connect_to_database():
#     sql = sqlite3.connect('C:/Users/Pc World G-210/Desktop/proj/crudapplication.db')
#     sql.row_factory = sqlite3.Row 
#     return sql 


# def get_database():
#     if not hasattr(g, 'crudapplication_db'):
#         g.crudapplication_db = connect_to_database()
#     return g.crudapplication_db

# mydb = mysql.connector.connect(host="localhost", user="root", passwd="password123")

# my_cursor = mydb.cursor()
# my_cursor.execute("CREATE DATABASE our_users")
# my_cursor.execute("SHOW DATABASES")

# for db in my_cursor:
#     print(db)

