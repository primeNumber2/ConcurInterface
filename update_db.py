import SQLConnector

sql_connector = SQLConnector.ms_sql


#The below scripts were divided into two parts, part1 update tbl_ConExpenseReports, part2 update tbl_ConcurExpenseDetails
#tbl_ConcurExpenseReports are updated base on the Report_Key difference between DW table and local table
#tbl_ConcurExpenseDetails are updated base on the Report_Key difference between Reports table and Details table

#part1
def update_tbl_concur_expense_reports():
    max_report_key = sql_connector.ExecQuery("SELECT MAX(Report_Key) FROM tbl_ConcurExpenseReports")[0][0]
    # remove the first column and the last column, id and insert_date are self-generated
    table_columns = sql_connector.ExecQuery("SELECT	a.name "
                                                   "FROM	syscolumns	a "
                                                   "JOIN	sysobjects	b "
                                                   "	ON		a.id = b.id "
                                                   "WHERE	b.name = 'tbl_ConcurExpenseReports'")[1:(-1)]
    #join the column names in list report_table_columns, using comma
    table_columns = ",".join([element[0] for element in table_columns])

    #generate the sql string
    insert_sql_string = "INSERT INTO tbl_ConcurExpenseReports (%s)  SELECT %s FROM " \
                        "Concur.DW_Master.MD.tbl_ConcurExpenseReports " \
                        "WHERE Employee_Ledger = '0506' " \
                        "AND Report_Key > %s" \
                        % (table_columns,table_columns, max_report_key)
    #udpdat the db and return the influenced rows number
    row_counts = sql_connector.ExecNoQuery(insert_sql_string)
    print str(row_counts) + " rows are updated"


#part2
def update_tbl_concur_expense_details():
    initial_key = sql_connector.ExecQuery("SELECT MAX(Report_Key) FROM tbl_ConcurExpenseDetails")[0][0]
    start_id = sql_connector.ExecQuery("SELECT id FROM tbl_ConcurExpenseReports WHERE Report_Key = %s"
                                       % initial_key)[0][0]
    end_id = sql_connector.ExecQuery("SELECT MAX(id) FROM tbl_ConcurExpenseReports")[0][0]
    if start_id == end_id:
        print "No new Report_Key generated"
        return 0
    table_columns = sql_connector.ExecQuery("SELECT	a.name "
                                            "FROM	syscolumns	a "
                                            "JOIN	sysobjects	b "
                                            "	ON		a.id = b.id "
                                            "WHERE	b.name = 'tbl_ConcurExpenseDetails'")[1:(-1)]
    table_columns = ",".join([element[0] for element in table_columns])
    print start_id, end_id, initial_key
    while(start_id < end_id):
        start_key = sql_connector.ExecQuery("SELECT Report_Key FROM tbl_ConcurExpenseReports WHERE id = %s" % start_id)[0][0]
        if end_id - start_id > 5:
            start_id += 5
        else:
            start_id = end_id
        end_key = sql_connector.ExecQuery("SELECT Report_Key FROM tbl_ConcurExpenseReports WHERE id = %s" % start_id)[0][0]
        row_counts = sql_connector.ExecNoQuery("INSERT INTO tbl_ConcurExpenseDetails(%s) SELECT * FROM "
                                              "Concur.DW_Master.MD.tbl_ConcurExpenseDetails "
                                              "WHERE Report_Key IN "
                                              "(SELECT Report_Key FROM tbl_ConcurExpenseReports "
                                              "WHERE Report_Key > %s "
                                              "AND  Report_Key <= %s )  " % (table_columns, start_key, end_key) )

        print "The start Key is " + str(start_key), "; The end key is " + str(end_key)
        print str(row_counts) + " rows are updated; ", str(end_id - start_id) + " Report_Keys are left"


if __name__ == "__main__":
    update_tbl_concur_expense_reports()
    update_tbl_concur_expense_details()