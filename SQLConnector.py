import pymssql

#
# HOST = 'SRVHOUSQL09\DW'
# USERNAME = 'MDReader_KingDee'
# PASSWORD = 're4dc0ncur'
# DATABASE_ADDRESS = 'DW_Master'

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
        self.conn = pymssql.connect(host=self.host, user=self.user, password = self.pwd, database = self.db, charset = "cp936")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, "connection failed")
        else:
            return cur
    # return a list consists of tuples
    def ExecQuery(self, sql_string):
        cur = self.__GetConnect()
        cur.execute(sql_string)
        result = cur.fetchall()
        self.conn.close()
        return result

    def ExecNoQuery(self, sql_string):
        cur = self.__GetConnect()
        cur.execute(sql_string)
        self.conn.commit()
        self.conn.close()
        return cur.rowcount


ms_sql = MSSQL(host=HOST, user=USERNAME, pwd=PASSWORD, db=DATABASE_ADDRESS)
