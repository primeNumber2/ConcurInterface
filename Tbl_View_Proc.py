# create two procedure in database
# The first is for query the expense details given the parameters ledger, start time and end time
# The second is for query the employees in concur details given the parameters ledger, start time and end time

import SQLConnector

sql_connector = SQLConnector.ms_sql_utf8
DATABASE = 'R_NPE_ForConcur_0724'


# The first proc
def update_ConcurExpenseReport(database):
    sql_connector.ExecNoQuery("Drop Proc proc_ConcurExpenseReport")
    sql_connector.ExecNoQuery(
    """
    CREATE PROC proc_ConcurExpenseReport
        @EmployLedger nvarchar(20),
        @StartDate datetime,
        @EndDate datetime

    AS
    (
    SELECT
            a.Report_Key,
            --a.Batch_ID,
            --a.Batch_Date,
            a.Employee_ID,
            a.Submit_Date,
            a.Last_Name,
            a.First_Name,
            c.FNumber,
            --取c.FNumber截止最后一个小数点之前的字符
            LEFT(c.FNumber, LEN(c.FNumber) - CHARINDEX( '.',  REVERSE(c.FNumber))) AS DeptNo,
            --a.Employee_Country,
            --a.Employee_BU,
            a.Employee_Ledger,
            --a.Employee_CostCenter,
            a.Employee_Currency,
            a.Report_Total,
            a.Business_Purpose,
            b.Expense_SubAccount,
            SUM(b.Expense_Payable)	AS	Payable,
            b.Expense_Currency,
            b.Expense_Exchange_Rate,
            SUM(b.Local_Currency_Net_Amount)	AS	Local_Currency_Net_Amount,
            a.Additional_Accounting_Info


    FROM	tbl_ConcurExpenseReports	a
    JOIN	tbl_ConcurExpenseDetails	b
        ON	a.Report_Key = b.Report_Key
    LEFT JOIN    %s.dbo.t_Emp c
        ON	a.Employee_ID = c.F_105	--F_105是自定义的字段，表示HCM_Number
    WHERE a.Employee_Country = 'CN'
    AND	a.Employee_Ledger = @EmployLedger
    AND	a.Submit_Date >= @StartDate
    AND	a.Submit_Date <= @EndDate

    GROUP BY
           a.Report_Key,
            a.Batch_ID,
            a.Batch_Date,
            a.Employee_ID,
            a.Submit_Date,
            a.Last_Name,
            a.First_Name,
            c.FNumber,
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
    )
    """ % database)


# The second proc
def update_Employee_Mapping_Table(database):
    # sql_connector.ExecNoQuery("Drop Proc proc_Employee_Mapping_Table")
    sql_connector.ExecNoQuery(
        """
        CREATE PROC proc_Employee_Mapping_Table
        @Ledger nvarchar(20),
        @StartDate datetime,
        @EndDate datetime
    AS
    SELECT DISTINCT	a.Last_Name,
                        a.First_Name,
                        a.Employee_ID,
                        b.FNumber,
                        b.FName
    FROM		tbl_ConcurExpenseReports a
    LEFT JOIN	%s.dbo.t_Emp b
        ON			a.Employee_ID = b.F_105
    WHERE	a.Employee_Ledger = @Ledger
    AND		a.Submit_Date >= @StartDate
    AND		a.Submit_Date <= @EndDate
    AND       b.FNumber is NULL
    ORDER BY a.Employee_ID
    """ % database
    )


# The second proc
def get_HCM_Number(database):
    sql_connector.ExecNoQuery("Drop Proc proc_Get_HCM_Number")
    sql_connector.ExecNoQuery(
        """
        CREATE PROC proc_Get_HCM_Number
        @Ledger nvarchar(20),
        @StartDate datetime,
        @EndDate datetime
    AS
    SELECT DISTINCT	a.Employee_ID

    FROM		tbl_ConcurExpenseReports a
    LEFT JOIN	%s.dbo.t_Emp b
        ON			a.Employee_ID = b.F_105
    WHERE	a.Employee_Ledger = @Ledger
    AND		a.Submit_Date >= @StartDate
    AND		a.Submit_Date <= @EndDate
    AND       b.FNumber IS NULL
    ORDER BY a.Employee_ID
    """ % database
    )


update_ConcurExpenseReport(DATABASE)
update_Employee_Mapping_Table(DATABASE)
get_HCM_Number(DATABASE)