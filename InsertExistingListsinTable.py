#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Created on Thu Jan 14 14:29:06 2016
@author: ncelik
"""
''' Connecting the database'''
import psycopg2  ## Source: http://www.stickpeople.com/projects/python/win-psycopg/   run 3.3 version

try:
    conn = psycopg2.connect("dbname='istekDB' user='*' host='localhost' password='*'")
    print  ("I am connected to the database")
except:
    print ("I am unable to connect to the database")

#conn.set_client_encoding('latin5')
cursor = conn.cursor()
conn.rollback()

birimListesi=[]
f = open(r'....BirimListesi.txt', 'r')
for line in f.readlines():
             #print line
        birimListesi.append(line)
f.close()

koordinatListesi=[]
koordinatIdListesi=[]
koordinatKoduListesi=[]
f = open(r'....KoordinatListesi.txt', 'r')
for line in f.readlines():
             #print line
        koordinatListesi.append(line.split())
        koordinatIdListesi.append(line.split()[0])
        koordinatKoduListesi.append(line.split()[1])
f.close()


formatListesi=[]
formatAdiListesi=[]
formatKoduListesi=[]
f = open(r'....FormatListesi.txt', 'r')
for line in f.readlines():
             #print line
        formatListesi.append(line.split())
        formatAdiListesi.append(line.split()[0])
        formatKoduListesi.append(line.split()[1])
f.close()




#selectquery ="SELECT * FROM birimler_listesi WHERE birimler_listesi.birim_adi= (%s)"
#cursor.execute(selectquery, birimListesi[1])
#record = cursor.fetchall()
#print record
#conn.commit()


#"select exists(select relname from pg_class where relname='" + table_str + "')"

selectquery ="select birim_adi from birimler_listesi where birim_adi='" + birimListesi[1] + "'"
cursor.execute(selectquery)
conn.commit()
# retrieve the records from the database
records = cursor.fetchall()


###This part select a query
def selectOneItemFromList(item,columnname,liste):
    selectquery ="select "+ columnname +" from " + liste+ " where " +columnname+ "="+"'" + item + "'"
    cursor.execute(selectquery)
    conn.commit()
    # retrieve the records from the database
    records = cursor.fetchall()
    return records



##this runs fuction above
print(selectOneItemFromList(birimListesi[1],"birim_adi","birimler_listesi"))


def selectAllRecordFromList(liste):
    cursor.execute("SELECT * FROM " +liste)
    # retrieve the records from the database
    records = cursor.fetchall()
    #return [i[1].encode('utf-8') for i in records]
    return [i[1] for i in records]

#print (selectAllRecordFromList("birimler_listesi"))


def insertListIntoDB(tablename,columnname,insertlist):
    insertquery ="INSERT INTO "+tablename+"("+columnname+") VALUES (%s);"
    for insertitem in insertlist:
        if insertitem not in selectAllRecordFromList(tablename):
            data = (insertitem)
            cursor.execute(insertquery, [data])
            conn.commit()
            print (insertitem+"has been inserted")
        else:
            print (insertitem+"already in the table and has not been inserted")
    #



def insertListIntoDB2(tablename,columnname,insertlist):
    columnnumber=len(columnname)
    if len(columnname)>1:
        count=1
        insertquerycolumnpart=""
        insertqueryspart=""
        insertquerylistpart=[]
        while count<=len(columnname):
           insertquerycolumnpart= insertquerycolumnpart+columnname[len(columnname)-count]+','
           insertqueryspart=insertqueryspart+ "%s,"
           insertquerylistpart.append(insertlist[len(columnname)-count])
           count=count+1

    insertquery ="INSERT INTO "+tablename+"("+insertquerycolumnpart[:-1]+") VALUES (" +insertqueryspart[:-1]+ ");"


    def createcurrectdata(idx,columnnumber,insertquerylistpart):
        count=columnnumber
        currentdata=()
        while count>0:
          currentdata= currentdata+(insertquerylistpart[columnnumber-count][idx],)
          count=count-1
          print (count)
        return currentdata


    for idx,item in enumerate(insertquerylistpart[0]):
        cursor.execute(insertquery,createcurrectdata(idx,columnnumber,insertquerylistpart))
        conn.commit()


insertListIntoDB("birimler_listesi","birim_adi",birimListesi[1:])
insertListIntoDB2("verikoordinat_listesi",["koordinatkodu","srid"],[koordinatKoduListesi[1:],koordinatIdListesi[1:]])
insertListIntoDB2("veriformat_listesi",["format_adi","format_kodu"],[formatAdiListesi[1:],formatKoduListesi[1:]])

##insertquery ="INSERT INTO birimler_listesi(birim_adi) VALUES (%s);"
##for birimadi in birimListesi[1:]:
##    if birimadi not in selectAllRecordFromList("birimler_listesi"):
##        data = (birimadi.encode("utf-8"))
##        cursor.execute(insertquery, [data])
##        conn.commit()
##        print (birimadi+"birimadi has been inserted")
##    else:
##        print (birimadi+"already in the table and has not been inserted")
###
##
