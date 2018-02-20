import sqlite3

connection= sqlite3.connect('data.db') #we are making our database in file

cursor=connection.cursor()

create_table="CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)


user=(1,'jose','asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query,user)

#to insert multiple rows do
users=[
    (2,'dose','assf'),
    (3,'jack','pope')
]
cursor.executemany(insert_query,users)

select_query= "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()