import sqlite3

connection = sqlite3.connect('user.db')
cursor = connection.cursor()

cmd1 = 'create table if not exists user(email varchar(40) primary key, name varchar(40) not null, password varchar(40) not null)'
cursor.execute(cmd1)

cmd2 = """insert into user(email,name, password)values('piyushprakash@gmail.com','piyush','piyush'),('nishankamath@gmail.com','nishan','nishan')"""
#cursor.execute(cmd2)
cmd3 = "select * from user"
ans = cursor.execute(cmd3)
connection.commit()
for i in ans:
    print(i)

connection.commit()

connection.close()