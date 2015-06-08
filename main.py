from flask import Flask
from flask import render_template
import SQLConnector

app = Flask(__name__)

names = ['frank', 'jack', 'john']


def sql_generate_table(ledger, start_date, end_date):
    # return the table of sql date
    sql_connector = SQLConnector.ms_sql
    sql_connector.exec_query( """SELECT top 10 a.Report_Key,
		a.Batch_ID,
		a.Batch_Date,
		a.Employee_ID,
		a.Submit_Date,
		a.Last_Name,
		a.First_Name,
		a.Employee_Country,
		a.Employee_BU,
		a.Employee_Ledger,
		a.Employee_CostCenter,
		a.Employee_Currency,
		a.Report_Total,
		a.Business_Purpose,
		a.Additional_Accounting_Info,
		b.Expense_SubAccount,
		SUM(b.Expense_Payable)	AS	Payable,
		b.Expense_Currency,
		b.Expense_Exchange_Rate,
		SUM(b.Local_Currency_Net_Amount)	AS	Local_Currency_Net_Amount

FROM	MD.tbl_ConcurExpenseReports	a
JOIN	MD.tbl_ConcurExpenseDetails b
	ON	a.Report_Key = b.Report_Key
WHERE a.Employee_Country = 'CN'
AND	a.Employee_Ledger = %s
AND	a.Submit_Date > '%s'
AND	a.Submit_Date < '%s'
GROUP BY

a.Report_Key,
		a.Batch_ID,
		a.Batch_Date,
		a.Employee_ID,
		a.Submit_Date,
		a.Last_Name,
		a.First_Name,
		a.Employee_Country,
		a.Employee_BU,
		a.Employee_Ledger,
		a.Employee_CostCenter,
		a.Employee_Currency,
		a.Report_Total,
		a.Business_Purpose,
		a.Additional_Accounting_Info,
		b.Expense_SubAccount,
		b.Tax1_Reclaim_Country,
		b.Expense_Currency,
		b.Expense_Exchange_Rate,
		b.Receipt_Type
""" % (ledger, start_date, end_date))

@app.route('/')
def index():
    return render_template('index.html', names = names)

if __name__ == "__main__":
    app.run('0.0.0.0', 8080, True)