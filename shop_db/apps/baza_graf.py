import os
import tkinter as tk
from tkinter import ttk, simpledialog
import psycopg2

baza = os.environ.get('PGDATABASE', 'sklep')
user = os.environ.get('PGUSER', 'postgres')

def wyswietl_dane():
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("SELECT imie, nazwisko, klient_id, nazwa_firmy, telefon, email FROM klient")
    rows = cursor.fetchall()

    for i in tree.get_children():
        tree.delete(i)

    for row in rows:
        tree.insert("", tk.END, values=row)

    conn.close()

root = tk.Tk()
root.title("Tabela z bazy danych")
root.geometry("800x600")

passw = simpledialog.askstring("Logowanie", "Podaj hasło do bazy danych:", show="*")
connection_string = "dbname = %s user =%s password=%s host=%s" % (baza, user, passw, os.environ.get('PGHOST', 'localhost'))

scroll_y = ttk.Scrollbar(root, orient="vertical")
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

cols = ("Imię", "Nazwisko", "Id", "Firma", "Telefon", "Email")
tree = ttk.Treeview(root, columns=cols, show="headings", yscrollcommand=scroll_y.set)
tree.pack(fill=tk.BOTH, expand=True)

scroll_y.config(command=tree.yview)

tree.heading("Imię", text="Imię")
tree.heading("Nazwisko", text="Nazwisko")
tree.heading("Id", text="Id")
tree.heading("Firma", text="Firma")
tree.heading("Telefon", text="Telefon")
tree.heading("Email", text="Email")

tree.column("Imię", width=50, anchor=tk.CENTER)
tree.column("Nazwisko", width=120)
tree.column("Id", width=30)
tree.column("Firma", width=100)
tree.column("Telefon", width=20)
tree.column("Email", width=100, anchor=tk.E)

btn_odswiez = tk.Button(root, text="Pokaż/Odśwież dane", command=wyswietl_dane)
btn_odswiez.pack(pady=10)

root.mainloop()
