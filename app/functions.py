import sqlite3
import time
import datetime

DATABASE_PATH = 'app/db.sqlite'


#fucntions
def check_message(message: str):
    if len(message) == 7 and message[3] == '-':
        return True
    return False


#bd functions
def send_answer(tg_id: str, text: str):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "UPDATE user SET vice_president_poll='"+text+"' WHERE tg_id='"+tg_id+"'"
    cursor.execute(sql)
    conn.commit()
    conn.close()


def look(text: str):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "SELECT * FROM user WHERE key='"+text+"'"
    cursor.execute(sql)
    result = cursor.fetchall()[0]
    conn.close()
    S = ''
    for i in result:
        S += str(i)+' '
    return S



def admin_send_answer(key: str, text: str):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        if text == '1':
            text='Анастасия Гуренко'
        elif text == '2':
            text='Генч Деніз'
        elif text == '3':
            text='Шиндер Михайло'
        elif text == '0':
            text = '0'
        else:
            return False
        sql = "UPDATE user SET vice_president_poll='"+text+"' WHERE key='"+key+"'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def check_code(text: str, tg_id: str):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "SELECT * FROM 'user' WHERE tg_id=='"+tg_id+"'"
    cursor.execute(sql)
    if(not len(cursor.fetchall()) == 0):
        return False
    cursor = conn.cursor()
    sql = "SELECT * FROM 'user' WHERE key=('"+str(text)+"') and tg_id=='0'"
    cursor.execute(sql)
    result = (not len(cursor.fetchall()) == 0)
    conn.close()
    return result


def commit_key(text: str, tg_id: str):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "UPDATE user SET tg_id='"+str(tg_id)+"' WHERE key='"+text+"'"
    cursor.execute(sql)
    conn.commit()
    conn.close()


def get_name(tg_id: str):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    sql = "SELECT * FROM user WHERE tg_id='"+tg_id+"'"
    cursor.execute(sql)
    result = cursor.fetchall()[0][1]
    conn.close()
    return result


if __name__ == "__main__":
    pass
