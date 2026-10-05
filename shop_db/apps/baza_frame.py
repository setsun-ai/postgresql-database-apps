import os
from tkinter import *
import psycopg2

baza = os.environ.get('PGDATABASE', 'sklep')
user = os.environ.get('PGUSER', 'postgres')
passw = os.environ.get('PGPASSWORD', '')

root = Tk()
root.title('Sklep z chemikaliami')
root.geometry("500x550")

def clear():
    f_name.delete(0, END)
    l_name.delete(0, END)

def query():
    conn = psycopg2.connect(host=os.environ.get('PGHOST', 'localhost'), database=baza, user=user, password=passw, port="5432")
    c = conn.cursor()
    c.execute("SELECT * FROM klient")
    records = c.fetchall()
    output = ''
    for record in records:
        output_label.config(text=f'{output}\n{record[0]} {record[1]}')
        output = output_label['text']
    conn.close()

def submit():
    conn = psycopg2.connect(host=os.environ.get('PGHOST', 'localhost'), database=baza, user=user, password=passw, port="5432")
    c = conn.cursor()
    thing1 = f_name.get()
    thing2 = l_name.get()
    c.execute("INSERT INTO klient (imie, nazwisko) VALUES (%s, %s)", (thing1, thing2))
    conn.commit()
    conn.close()
    query()
    clear()

my_frame = LabelFrame(root, text="Dodaj klienta")
my_frame.pack(pady=20)

f_label = Label(my_frame, text="Imię:")
f_label.grid(row=0, column=0, pady=10, padx=10)
f_name = Entry(my_frame, font=("Helvetica", 18))
f_name.grid(row=0, column=1, pady=10, padx=10)

l_label = Label(my_frame, text="Nazwisko:")
l_label.grid(row=1, column=0, pady=10, padx=10)
l_name = Entry(my_frame, font=("Helvetica", 18))
l_name.grid(row=1, column=1, pady=10, padx=10)

submit_button = Button(my_frame, text="Dodaj", command=submit)
submit_button.grid(row=2, column=0, pady=10, padx=10)

update_button = Button(my_frame, text="Odśwież", command=query)
update_button.grid(row=2, column=1, pady=10, padx=10)

output_label = Label(root, text="")
output_label.pack(pady=50)

query()
root.mainloop()
