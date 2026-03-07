import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_name=os.getenv('DB_Name')
def init_db():
    conn=sqlite3.connect(db_name)
    cursor=conn.cursor()
    cursor.execute("create table if not exists Subscribers (user_id Integer Primary key)")
    conn.commit()
    conn.close()

def add_subscriber(id):
    conn=sqlite3.connect(db_name)
    cursor=conn.cursor()
    cursor.execute('''
    Insert or ignore into Subscribers(user_id) values (?) 
''',(id,))
    conn.commit()
    conn.close()

def get_subscriber():
    conn=sqlite3.connect(db_name)
    cursor=conn.cursor()
    cursor.execute('select user_id from Subscribers')
    users=[rows[0] for rows in cursor.fetchall()]
    conn.close()
    return users
    
