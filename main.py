from flask import Flask
from flask import render_template
import SQLConnector
from flask import request

app = Flask(__name__)


def sql_generate_table(ledger, start_date, end_date):
    # return the table of concur data, include the expense information, aim to generate vouchers
    sql_connector = SQLConnector.ms_sql
    data_table = sql_connector.ExecQuery("EXEC proc_ConcurExpenseReport '%s', '%s', '%s'" %
                                          (ledger, start_date, end_date))
    return data_table

def sql_get_employee(ledger, start_date, end_date):
    # generate distinct employee information under certain period, let users to update the link between concur user and
    # Kingdee users
    sql_connector = SQLConnector.ms_sql
    employee_table = sql_connector.ExecQuery("SELECT DISTINCT ")


#The column names here will be the same with the procedure in sql
col_names = ['No', 'Report_Key', 'Employee_ID', 'Submit_Date', 'Last_Name', 'First_Name', 'Kingdee_Number',
             'Kingdee_Department', 'Employee_Ledger', 'Employee_Currency',
             'Report_Total', 'Business_Purpose', 'Additional_Accounting_Info', 'Expense_SubAccount', 'Payable',
             'Expense_Currency', 'Expense_Exchange_Rate', 'Local_Currency_Net_Amount']


@app.route('/employee', methods=['GET', 'POST'] )
def employee():
    if request.method == 'POST':
        ledger = request.form['ledger']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        return render_template('employee.html')
    else:
        return render_template('employee.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        ledger = request.form['ledger']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        table = sql_generate_table(ledger, start_date, end_date)
        return render_template('data.html', ledger=ledger, start_date=start_date, end_date=end_date,
                               col_names=col_names, table=table)
    else:
        return render_template('data.html')


if __name__ == "__main__":
    app.run('0.0.0.0', 5000, True)