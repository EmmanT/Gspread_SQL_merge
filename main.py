# user defined modules
import goauth as gfile
import sqlauth as sqlfile

import pymssql,sys
import datetime
now = datetime.datetime.now()


def workbook_lookup(credential,file):
    print datetime.datetime.now(), ' Loading Credentials'
    wrkbk = credential.open_by_url(file)
    wks = wrkbk.worksheet("Recoverable Leaks")
    lists = wks.get_all_values()
    return lists, wrkbk

def get_ratingmetric_sql():
    print datetime.datetime.now(), ' Gathering SQL data'
    vhost, vuser, vpass, vdb, query, listcolnames = sqlfile.sqlauth()
    conn = pymssql.connect(host=vhost, user=vuser, password=vpass, database=vdb, as_dict=True)
    cur = conn.cursor(as_dict=True)
    cur.execute(query)
    cur_list = cur.fetchall()
    conn.close()
    return cur_list, listcolnames

if __name__ == "__main__":
    #local variables
    sheetrow = 1
    inc = 1

    # get google dev credentials
    cred, file_url = gfile.auth()

    #get results of sql data
    query_result, colnames = get_ratingmetric_sql()
    colname = colnames.split(",")
    query_result = [[row[colname[0]],row[colname[1]],row[colname[2]],row[colname[3]],row[colname[4]],row[colname[5]],\
             row[colname[6]],row[colname[7]],row[colname[8]],row[colname[9]],row[colname[10]]] for row in query_result]


    #gathering data sheet information
    datasheet, wrkbk = workbook_lookup(cred, file_url)
    print datetime.datetime.now(), ' Creating new worksheet'
    worksheet = wrkbk.add_worksheet(title=str(now.year) + "/" + str(now.month)+ "/" + str(now.day) + "_" \
            + str(now.hour) + ":" + str(now.minute),rows =len(datasheet), cols = "100")

    #Store merged data to a new sheet in the same Google spreadsheet workbook.
    #column definition creation
    print datetime.datetime.now(), ' Populating column headers'
    col_value = colname
    col_list = worksheet.range('A1:M1')
    for i, val in enumerate(col_value):
        col_list[i].value = val
    worksheet.update_cells(col_list)

    #row population
    print datetime.datetime.now(), ' Storing data to the new worksheet'
    for n, sublists in enumerate(datasheet):
        for qrow in query_result:
            if str(qrow[0]) == str(sublists[3]) and str(qrow[1]) == str(sublists[11]):
                print ("%s Found (BOL --- %s)  #####  (ChargeCode --- %s)"\
                       % (str(round((float(n)/float(len(datasheet)))*100,2)) +'% Complete',sublists[3],sublists[11]))
                sheetrow = sheetrow+1
                cell_values = qrow +[sublists[1]] +[sublists[2]]
                cell_list = worksheet.range('A'+str(sheetrow)+':M'+str(sheetrow))
                for i, val in enumerate(cell_values): #gives us a tuple of an index and value
                    cell_list[i].value = val  #use the index on cell_list and the val from cell_values
                worksheet.update_cells(cell_list)


