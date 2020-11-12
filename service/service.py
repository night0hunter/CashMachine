from datetime import datetime
import sqlite3
import cfg


def create_log(log_name):
    con = sqlite3.connect(cfg.DB_NAME)
    cur = con.cursor()
    sql = ("""INSERT INTO logs(operation_name, operation_date) VALUES(?,?)""")
    result = cur.execute(sql, [log_name, datetime.today().strftime('%d.%m.%YT%H:%M:%S')])
    print(result)
    con.commit()
    con.close()
