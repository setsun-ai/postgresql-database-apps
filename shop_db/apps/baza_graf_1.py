import os
import tkinter as tk
from tkinter import ttk, simpledialog
import psycopg2

baza = os.environ.get('PGDATABASE', 'sklep')
user = os.environ.get('PGUSER', 'postgres')

def pobierz_dane():
    global connection_string

    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM raport2")
    rows = cursor.fetchall()

    nkols = [desc[0] for desc in cursor.description]
    conn.close()
    return (rows, nkols)

def wyswietl_dane():
    (rows, nkols) = pobierz_dane()

    for i in tree.get_children():
        tree.delete(i)

    for row in rows:
        tree.insert("", tk.END, values=row)

root = tk.Tk()
root.title("Tabela z bazy danych")
root.geometry("800x600")

passw = simpledialog.askstring("Logowanie", "Podaj hasło do bazy danych:", show="*")
connection_string = "dbname=%s user=%s password=%s host=%s" % (baza, user, passw, os.environ.get('PGHOST', 'localhost'))

scroll_y = ttk.Scrollbar(root, orient="vertical")
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

(rows, cols) = pobierz_dane()

tree = ttk.Treeview(root, columns=cols, show="headings", yscrollcommand=scroll_y.set)
tree.pack(fill=tk.BOTH, expand=True)

scroll_y.config(command=tree.yview)

for k in cols:
    tree.heading(k, text=k)

for k in cols:
    tree.column(k, width=100)

btn_odswiez = tk.Button(root, text="Pokaż/Odśwież dane", command=wyswietl_dane)
btn_odswiez.pack(pady=10)

root.mainloop()
