import SQLConnector
import sql_string

HOST_DW = 'SRVHOUSQL09\DW'
USERNAME_DW = 'MDReader_KingDee'
PASSWORD_DW = 're4dc0ncur'
DATABASE_ADDRESS_DW = 'DW_Master'

HOST_K3SH = 'SRVSHASQL01'
USERNAME_K3SH = 'appIntf'
PASSWORD_K3SH = 'N0v1terp'
DATABASE_ADDRESS_K3SH = 'Interface'

DW_Conn = SQLConnector.MSSQL(HOST_DW, USERNAME_DW, PASSWORD_DW, DATABASE_ADDRESS_DW)
K3SH_Conn = SQLConnector.MSSQL(HOST_K3SH, USERNAME_K3SH, PASSWORD_K3SH, DATABASE_ADDRESS_K3SH)

dw_data = DW_Conn.ExecQuery(sql_string.Query_Reports)
print dw_data[0]
insert_sql = "Insert into tbl_ConcurExpenseReports values ( "
for value in dw_data[0]:
    print value
    insert_sql += str(value) + ","
insert_sql += ")"
print insert_sql
# K3SH_Conn.ExecNoQuery(insert_sql)
