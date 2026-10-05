#!/usr/bin/python3
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import psycopg2
import getpass

baza = os.environ.get('PGDATABASE', 'sklep')
user = os.environ.get('PGUSER', 'postgres')
passw = getpass.getpass("Haslo do bazy: ")
connection_string = "dbname=%s user=%s password=%s host=%s" % (baza, user, passw, os.environ.get('PGHOST', 'localhost'))
conn = psycopg2.connect(connection_string)

def dodaj_towar():
    nazwa = simpledialog.askstring("Nowy towar", "Podaj nazwę towaru:")
    if not nazwa:
        return
    cena = simpledialog.askstring("Nowy towar", "Podaj cenę netto:")
    if not cena:
        return
    vat = simpledialog.askstring("Nowy towar", "Podaj VAT (np. 23):")
    if not vat:
        return
    idkat = simpledialog.askstring("Nowy towar", "Podaj ID kategorii:")
    if not idkat:
        return
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO towar(nazwa, cena_netto, vat, idkategoria) VALUES (%s, %s, %s, %s)",
                    (nazwa, cena, vat, idkat))
        conn.commit()
        cur.close()
        messagebox.showinfo("OK", "Towar dodany!")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Błąd", str(e))

def dodaj_kategorie():
    nazwa = simpledialog.askstring("Nowa kategoria", "Podaj nazwę kategorii:")
    if not nazwa:
        return
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO kategoria(nazwa) VALUES (%s)", (nazwa,))
        conn.commit()
        cur.close()
        messagebox.showinfo("OK", "Kategoria dodana!")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Błąd", str(e))

def dodaj_adres():
    ulica = simpledialog.askstring("Nowy adres", "Ulica:")
    if not ulica:
        return
    numer = simpledialog.askstring("Nowy adres", "Numer:")
    kod = simpledialog.askstring("Nowy adres", "Kod pocztowy:")
    miejscowosc = simpledialog.askstring("Nowy adres", "Miejscowość:")
    woj = simpledialog.askstring("Nowy adres", "Województwo:")
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO adres(ulica, numer, kod, miejscowosc, wojewodztwo) VALUES (%s, %s, %s, %s, %s)",
                    (ulica, numer, kod, miejscowosc, woj))
        conn.commit()
        cur.close()
        messagebox.showinfo("OK", "Adres dodany!")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Błąd", str(e))

root = tk.Tk()
root.title("Sklep z chemikaliami")
root.geometry("300x200")

label_info = tk.Label(root, text="Nasz sklep", font=("Arial", 12))
label_info.pack(pady=20)

btn_nowy_towar = tk.Button(root, text="Dodaj nowy towar (+)", command=dodaj_towar, bg="green", fg="white")
btn_nowy_towar.pack(pady=5)

btn_nowakat = tk.Button(root, text="Dodaj kategorię (+)", command=dodaj_kategorie, bg="green", fg="white")
btn_nowakat.pack(pady=5)

btn_adres = tk.Button(root, text="Dodaj adres klienta (+)", command=dodaj_adres, bg="blue", fg="white")
btn_adres.pack(pady=5)

root.mainloop()
