#-------------------------------------------------------------------------------
# Author:      ncelik
# Created:     19.01.2016
#-------------------------------------------------------------------------------
import psycopg2
conn = psycopg2.connect("dbname='istekDB' user='*' host='localhost' password='*'")
conn_cursor = conn.cursor()

def selectAllRecordFromList(liste,conn_cursor):
    conn_cursor.execute("SELECT * FROM " +liste)
    # retrieve the records from the database
    records = conn_cursor.fetchall()
    colnames = [desc[0] for desc in conn_cursor.description]
    #return [i[1].encode('utf-8') for i in records]
    return records,colnames

def show_records_dict(liste,conn_cursor):
    records,colnames=selectAllRecordFromList(liste,conn_cursor)
    rows_list=[]
    for row in records:
        rows_dict = {}
        for idx,colname in enumerate(colnames):
            #rows_dict[colname] = [row[idx] for row in records] # gets each column in seperate list
            rows_dict[colnames[idx]] = row[idx]
        rows_list.append(rows_dict)
        #Generate dict from data provided
    return rows_dict,rows_list

'''Alternative section in below comment but you need to know the colomn number of list'''
##    for row in records:
##        rows_dict = {}
##        #rows_dict[colname] = [row[idx] for row in records] # gets each column in seperate list
##        rows_dict[colnames[0]] = row[0]
##        rows_dict[colnames[1]] = row[1]
##        rows_dict[colnames[2]] = row[2]
##        rows_dict[colnames[3]] = row[3]
##        rows_list.append(rows_dict)
##
##        #Generate dict from data provided
##    return rows_dict,rows_list

def show_records_list(liste,conn_cursor):
    allRecords=selectAllRecordFromList(liste,conn_cursor)
    rows_list = []
    for row in allRecords:
        rows_list.append(row)
    return rows_list

def insertIntoListByOne(liste,conn_cursor):
##    insertquery ="INSERT INTO "+tablename+"("+columnname+") VALUES (%s);"
    records,colnames=selectAllRecordFromList(liste,conn_cursor)
    print ("Mevcut Veriler")
    try:
        print_records_list(liste,conn_cursor)
    except:
        print ("Cant display any value")
    alreadyInThere=input("Eklemek istediginiz veri mevcut mu? E/H")
    if alreadyInThere=="E":
        pass
    elif alreadyInThere=="H":
        inputnames={}
        print ("veri eklenecek")
        colnamequerypart=""
        for idx,colname in enumerate(colnames[1:]):
             if "birim" in colname:
                 print_records_list("birimler_listesi",conn_cursor)
             if "veriformat" in colname:
                 print_records_list("veriformat_listesi",conn_cursor)
             if "verikoordinat" in colname:
                 print_records_list("verikoordinat_listesi",conn_cursor)
             if "sahibi" in colname:
                 print_records_list("isteksahibi_listesi",conn_cursor)
             if "tarihi" in colname:
                 print ( "tarih verisini yil-ay-gun seklinde giriniz")
             if  colname.endswith("istekgiristarihi"):
                 continue

             inputnames[idx]=input(colname+':').capitalize()
             if inputnames[idx]=="":
                    inputnames[idx]=None
             elif inputnames[idx]=="T" and "_tf" in colname:
                    inputnames[idx]=True
             elif inputnames[idx]=="F" and "_tf" in colname:
                    inputnames[idx]=False

             colnamequerypart=colnamequerypart+colname +","
        print (inputnames)
        insertquerypart=""
        for inputname in inputnames:
            insertquerypart=insertquerypart+"%s"+","
        print (insertquerypart)
        print ([inputnames[inputname] for inputname in inputnames])
        insertquery ="INSERT INTO "+liste+"("+colnamequerypart[:-1]+") VALUES (" +insertquerypart[:-1]+ ");"
        print (insertquery)
        conn_cursor.execute(insertquery,[inputnames[inputname] for inputname in inputnames])
        conn.commit()

def alterInListByOne():
    records,colnames=selectAllRecordFromList(liste,conn_cursor)
    print ("Mevcut Veriler")
    print_records_list(liste,conn_cursor)
    print ("Select one of the options below to alter the table")
    alreadyInThere=input("Eklemek istediginiz veri mevcut mu? E/H")


def print_records_list(liste,conn_cursor):
    mydict,mylist=show_records_dict(liste,conn_cursor)
    for idx, item in enumerate(mylist):
        print (mylist[idx])
        ##        print (mylist[idx].keys())
        ##        print (mylist[idx].values())
        ##        print (mylist[idx].items())
        ##        print (list(mylist[idx].items())[0])

def main():
    #print_records_list("isteksahibi_listesi",conn_cursor)
    #show_records_dict("isteksahibi_listesi",conn_cursor)
    print_records_list("birimler_listesi",conn_cursor)
    #insertIntoListByOne("isteksahibi_listesi",conn_cursor)
    insertIntoListByOne("istek_listesi",conn_cursor)
if __name__ == '__main__':
    main()
