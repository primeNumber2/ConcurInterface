from flask import Flask
from flask import render_template
import SQLConnector
from flask import request

app = Flask(__name__)


def sql_generate_table(ledger, start_date, end_date):
    # return the table of sql date
    sql_connector = SQLConnector.ms_sql
    data_table = sql_connector.ExecQuery( """SELECT
       --a.Report_Key,
		--a.Batch_ID,
		--a.Batch_Date,
		a.Employee_ID,
		a.Submit_Date,
		a.Last_Name,
		a.First_Name,
		--a.Employee_Country,
		--a.Employee_BU,
		a.Employee_Ledger,
		--a.Employee_CostCenter,
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
    return data_table

# table = sql_generate_table('0506', '2015-06-01', '2015-06-03')
col_names = ['No','Employee_ID','Submit_Date','Last_Name', 'First_Name','Employee_Ledger','Employee_Currency','Report_Total','Business_Purpose',
             'Additional_Accounting_Info','Expense_SubAccount','Payable','Expense_Currency','Expense_Exchange_Rate','Local_Currency_Net_Amount']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ledger = request.form['ledger'];
        start_date = request.form['start_date'];
        end_date = request.form['end_date'];
        table = sql_generate_table(ledger, start_date, end_date)
        return  render_template('index.html', col_names=col_names, table=table)
    else:
        return render_template('index.html', col_names=[], table=[])



if __name__ == "__main__":
    app.run('0.0.0.0', 8080, True)