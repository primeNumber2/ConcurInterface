from flask import Flask
from flask import render_template
import SQLConnector
from flask import request, redirect, url_for, session

app = Flask(__name__)

DATABASE = 'R_NPE_ForConcur_0724'


def sql_generate_expense_detail(ledger, start_date, end_date):
    # return the table of concur data, include the expense information, aim to generate vouchers
    sql_connector = SQLConnector.ms_sql_utf8
    data_table = sql_connector.ExecQuery("EXEC proc_ConcurExpenseReport '%s', '%s', '%s'" %
                                        (ledger, start_date, end_date))
    return data_table


def sql_get_employee(ledger, start_date, end_date):
    """
    generate distinct employee information under certain period, let users to update the mapping table
    between concur user and Kingdee users
    """
    sql_connector = SQLConnector.ms_sql_cp936
    employee_table = sql_connector.ExecQuery("Exec proc_Employee_Mapping_Table '%s', '%s', '%s'" %
                                        (ledger, start_date, end_date))
    hcm_numbers = sql_connector.ExecQuery("Exec proc_get_HCM_Number '%s', '%s', '%s'" % (ledger, start_date, end_date))
    return hcm_numbers, employee_table


def update_hcm_number(kingdee_number, hcm_number):
    sql_connector = SQLConnector.ms_sql_utf8
    rows = sql_connector.ExecNoQuery("UPDATE %s.dbo.t_emp SET F_105 = '%s' WHERE FNumber = '%s'"
                              % (DATABASE, hcm_number, kingdee_number))
    return rows


def sql_get_valid_department():
    sql_connector = SQLConnector.ms_sql_utf8
    valid_departments = sql_connector.ExecQuery("SELECT FNumber FROM %s.dbo.t_department"
                                     % (DATABASE))
    return valid_departments


@app.route('/employee', methods=['GET', 'POST'])
def employee():
    col_names = ['No', 'Last_Name', 'First_Name', "Employee_ID", "Kingdee_Number", "Kingdee_Name"]
    ledger = session['ledger']
    start_date = session['start_date']
    end_date = session['end_date']

    if request.method == 'GET':
        table = sql_get_employee(ledger=ledger, start_date=start_date, end_date=end_date)[1]
        return render_template('employee.html', ledger=ledger, start_date=start_date, end_date=end_date,
                               table=table, col_names=col_names)
    if request.method == 'POST':
        kingdee_numbers = request.form.getlist('Kingdee_No')
        hcm_numbers = sql_get_employee(ledger=ledger, start_date=start_date, end_date=end_date)[0]
        # for num in range(len(emp)):
        hcm_numbers = list(map(lambda x:str(x[0]), hcm_numbers))
        influenced_rows = 0
        for kingdee_number, hcm_number in zip(kingdee_numbers, hcm_numbers):
            if kingdee_number != "":
                influenced_rows += update_hcm_number(kingdee_number, hcm_number)
        table = sql_get_employee(ledger=ledger, start_date=start_date, end_date=end_date)[1]
        return render_template('employee.html', ledger=ledger, start_date=start_date, end_date=end_date,
                           table=table, col_names=col_names, influenced_rows=influenced_rows)


@app.route('/data', methods=['GET', 'POST'])
def data():
    #The column names here will be the same with the procedure in sql
    col_names = ['No', 'Report_Key', 'Employee_ID', 'Submit_Date', 'Last_Name', 'First_Name', 'Kingdee_Number',
             'Kingdee_Department', 'Employee_Ledger', 'Employee_Currency',
             'Report_Total', 'Business_Purpose', 'Expense_SubAccount', 'Payable',
             'Expense_Currency', 'Expense_Exchange_Rate', 'Local_Currency_Net_Amount', 'Additional_Accounting_Info',
             'Department', 'Project1', 'Project2', 'Project3', 'Project4', 'Project5']
    if request.method == 'POST':
        ledger = request.form['ledger']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        table = sql_generate_expense_detail(ledger, start_date, end_date)
        if request.form['bt'] == 'data':
            return render_template('data.html', ledger=ledger, start_date=start_date, end_date=end_date,
                                   col_names=col_names, table=table)
        elif request.form['bt'] == 'employee':
            session['ledger'] = ledger
            session['start_date'] = start_date
            session['end_date'] = end_date
            return redirect(url_for('employee'))
        elif request.form['bt'] == 'check':
            # departments = request.form.getlist('department')
            valid_departments = sql_get_valid_department()
            valid_departments = list(map(lambda x:str(x[0]), valid_departments))
            s = ""
            for i in valid_departments:
                s += i
            return s
    else:
        return render_template('data.html')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run('0.0.0.0', 5000, True)