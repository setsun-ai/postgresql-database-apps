#!/usr/bin/python3
import os
import sys
import psycopg2
import getpass

baza = os.environ.get('PGDATABASE', 'sklep')
user = os.environ.get('PGUSER', 'postgres')
passw = getpass.getpass("Haslo: ")

connection_string = "dbname=%s user=%s password=%s host=%s" % (baza, user, passw, os.environ.get('PGHOST', 'localhost'))
conn = psycopg2.connect(connection_string)
cur = conn.cursor()

cur.execute("select * from klient")
header = [i[0] for i in cur.description]
print(header)
cur.copy_to(sys.stdout, 'klient', sep='\t', null='NULL')

cur.execute("select * from raport2")
table = cur.fetchall()
print(table)

cur.close()
conn.commit()
