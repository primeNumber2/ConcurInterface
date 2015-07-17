from flask import Flask
from flask import render_template
import pymssql

HOST = 'SRVSHASQL01'
USERNAME = 'appadmin'
PASSWORD = 'N0v1terp'
DATABASE_ADDRESS = 'ConcurInt'

class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError, "No database information")
        self.conn = pymssql.connect(host = self.host, user=self.user, password = self.pwd, database = self.db, charset = "utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, "connection failed")
        else:
            return cur

    def ExecQuery(self, sql_string):
        cur = self.__GetConnect()
        cur.execute(sql_string)
        result = cur.fetchall()
        self.conn.close()
        return cur.rowcount

    def ExecNoQuery(self, sql_string):
        cur = self.__GetConnect()
        cur.execute(sql_string)
        self.conn.commit()
        self.conn.close()

ms_sql = MSSQL(host=HOST, user=USERNAME, pwd=PASSWORD, db=DATABASE_ADDRESS)

print ms_sql.ExecQuery("SELECT * FROM tbl_ConcurExpenseReports")

# app = Flask(__name__)
#
#
# def sql_generate_table(ledger, start_date, end_date):
#     data = MSSQL(host=HOST, user=USERNAME, pwd=PASSWORD, db=DATABASE_ADDRESS)
#     data_result = data.ExecQuery("EXEC proc_ConcurExpenseReport '%s', '%s', '%s'" % (ledger, start_date, end_date))
#     return data_result
#
# table = sql_generate_table('0506', '2015-07-01', '2015-07-15')
# print len(table)

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     return render_template('fortest.html', table = table )
#
# if __name__=="__main__":
#     app.run("0.0.0.0", 5000, True)
