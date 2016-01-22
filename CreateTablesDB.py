#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Created on Wed Jan 13 09:29:38 2016

@author: ncelik
"""

''' Connecting the database'''
import psycopg2

try:
    conn = psycopg2.connect("dbname='istekDB' user='*' host='localhost' password='*'")
    print  ("I am connected to the database")
except:
    print ("I am unable to connect to the database")

cursor = conn.cursor()


###FUNCTION CHECKS IF TABLE EXIST
##Source:   http://stackoverflow.com/questions/1874113/checking-if-a-postgresql-table-exists-under-python-and-probably-psycopg2
def table_exists(con, table_str):
    exists = False
    try:
        cur = con.cursor()
        cur.execute("select exists(select relname from pg_class where relname='" + table_str + "')")
        exists = cur.fetchone()[0]
        print (exists)
        cur.close()
    except psycopg2.Error as e:
        print (e)
    return exists

###FUNCTION CHECKS IF TABLE EXIST ELSE CREATE ONE with given query
def checkexistelsecreatetable(tablename,tablecreatequery):
        if table_exists(conn, tablename):
            print ("Table already exists")
        else:
            cursor.execute(tablecreatequery)
            conn.commit()
            print (tablename + " has been created")




###Query to create table birimler listesi###
createBirimTableQuery="""
CREATE TABLE birimler_listesi
(
  birim_id serial NOT NULL,
  birim_adi character varying(64),
  CONSTRAINT birim_id_pkey PRIMARY KEY (birim_id)
)
WITH (
  OIDS=FALSE
);

"""

###Query for create is isteksahibi listesi###
createIstekSahibiTableQuery='''
CREATE TABLE isteksahibi_listesi
(
  isteksahibi_id serial NOT NULL,
  isteksahibi_adi character varying(64),
  isteksahibi_soyadi character varying(64),
  isteksahibi_birimid integer,
  CONSTRAINT isteksahibi_id_pkey PRIMARY KEY (isteksahibi_id),
  CONSTRAINT isteksahibi_listesi_isteksahibi_birimid_fkey FOREIGN KEY (isteksahibi_birimid)
      REFERENCES birimler_listesi (birim_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
'''
###Query for create is verikoordinat listesi###
createVeriKoordinatTableQuery='''
CREATE TABLE verikoordinat_listesi
(
  sr_id integer NOT NULL,
  koordinatkodu character varying(20),
  CONSTRAINT srid_pkey PRIMARY KEY (srid)
)
WITH (
  OIDS=FALSE
);'''

###Query for create is veriformat listesi###
createVeriFormatTableQuery='''
CREATE TABLE veriformat_listesi
(
  format_id serial NOT NULL,
  format_adi character varying(64),
  format_kodu character varying(32),
  CONSTRAINT format_id_pkey PRIMARY KEY (format_id)
)
WITH (
  OIDS=FALSE
);
'''
###Query for create is istek listesi###
createIsIstekTableQuery='''
CREATE TABLE istek_listesi
(
  istek_id serial NOT NULL,
  istek_adi character varying(64),
  istek_veriformatid integer,
  istektaleptarihi date,
  istekteslimtarihi date,
  istek_sahibiid integer,
  istek_aciklama character varying,
  istek_verikoordinatid integer,
  istek_veridonusum_tf boolean,
  istek_veriyolu character varying,
  istek_bilgigiristarihi timestamp without time zone DEFAULT now(),
  CONSTRAINT istek_id_pkey PRIMARY KEY (istek_id),
  CONSTRAINT istek_listesi_istek_sahibiid_fkey FOREIGN KEY (istek_sahibiid)
      REFERENCES isteksahibi_listesi (isteksahibi_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
'''


createIsIstek_LogTableQuery='''
create table istek_log (
istek_id integer,
theaction character,
changetime timestamp default NOW());'''



createRuleIsIstek_LogTableQuery='''
create rule istek_delete_log2 as on delete to istek_listesi
  do insert into istek_log values (old.istek_id,'D');

create rule istek_update_log2 as on update to istek_listesi
  do insert into istek_log values (old.istek_id,'U');
'''


def createRules(createRuleIsIstek_LogTableQuery):
            cursor.execute(createRuleIsIstek_LogTableQuery)
            conn.commit()
            print ("Rules" + " has been created")



"""
create rule istek_delete_log as on delete to istek_listesi
  do insert into istek_log values (old.istek_id,'D');

create rule istek_update_log as on update to istek_listesi
  do insert into istek_log values (old.istek_id,'U');
"""




checkexistelsecreatetable("birimler_listesi",createBirimTableQuery)
checkexistelsecreatetable("isteksahibi_listesi",createIstekSahibiTableQuery)
checkexistelsecreatetable("veriformat_listesi",createVeriFormatTableQuery)
checkexistelsecreatetable("verikoordinat_listesi",createVeriKoordinatTableQuery)
checkexistelsecreatetable("istek_listesi",createIsIstekTableQuery)
checkexistelsecreatetable("istek_log2",createIsIstekTableQuery)
createRules(createRuleIsIstek_LogTableQuery)
