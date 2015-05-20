import sqlite_manager 
db_conn = sqlite_manager.get_db_connection("data.sqlite")  
f = open("manga_info",'r').readlines()
for m in f:
    m = m.rstrip("\n")
    m = m.split(":")
    print m
    sqlite_manager.insert_manga(db_conn, m[0], m[1], m[2])
