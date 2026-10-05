import os
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import psycopg2

baza = os.environ.get('PGDATABASE', 'sklep')
user = os.environ.get('PGUSER', 'postgres')

passw = simpledialog.askstring("Logowanie", "Podaj hasło do bazy danych:", show="*")
connection_string = "dbname=%s user=%s password=%s host=%s" % (baza, user, passw, os.environ.get('PGHOST', 'localhost'))

def pobierz_polaczenie():
    return psycopg2.connect(connection_string)

lista_kategorii = []
lista_vat = []

def pobierz_vat_z_bazy():
    global lista_vat
    try:
        conn = pobierz_polaczenie()
        cursor = conn.cursor()
        cursor.execute("SELECT idstawki, st_vat FROM stawkivat ORDER BY st_vat;")
        lista_vat = cursor.fetchall()
        cursor.close()
        conn.close()
        return [str(vat[1]) for vat in lista_vat]
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się pobrać stawek VAT z bazy:\n{e}")
        return []

def pobierz_kategorie_z_bazy():
    global lista_kategorii
    try:
        conn = pobierz_polaczenie()
        cursor = conn.cursor()
        cursor.execute("SELECT kategoria_id, nazwa FROM kategoria ORDER BY nazwa;")
        lista_kategorii = cursor.fetchall()
        cursor.close()
        conn.close()
        return [kat[1] for kat in lista_kategorii]
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się pobrać kategorii z bazy:\n{e}")
        return []

def dodaj_towar():
    okno_dodaj = tk.Toplevel(root)
    okno_dodaj.title("Dodaj nowy towar")
    okno_dodaj.geometry("350x300")
    okno_dodaj.grab_set()

    frame = tk.Frame(okno_dodaj)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Nazwa towaru:").grid(row=0, column=0, sticky=tk.W, pady=5)
    entry_nazwa = tk.Entry(frame, width=25)
    entry_nazwa.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Cena netto:").grid(row=1, column=0, sticky=tk.W, pady=5)
    entry_cena = tk.Entry(frame, width=25)
    entry_cena.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="VAT:").grid(row=2, column=0, sticky=tk.W, pady=5)
    nazwy_vat = pobierz_vat_z_bazy()
    combo_vat = ttk.Combobox(frame, values=nazwy_vat, width=22, state="readonly")
    combo_vat.grid(row=2, column=1, pady=5)
    if nazwy_vat:
        combo_vat.current(0)

    tk.Label(frame, text="Kategoria:").grid(row=3, column=0, sticky=tk.W, pady=5)
    nazwy_kategorii = pobierz_kategorie_z_bazy()
    combo_kategoria = ttk.Combobox(frame, values=nazwy_kategorii, width=22, state="readonly")
    combo_kategoria.grid(row=3, column=1, pady=5)
    if nazwy_kategorii:
        combo_kategoria.current(0)

    def zapisz_do_bazy():
        nazwa = entry_nazwa.get().strip()
        cena = entry_cena.get().strip()
        idx_vat = combo_vat.current()
        idx_kat = combo_kategoria.current()

        if not (nazwa and cena):
            messagebox.showwarning("Błąd", "Wszystkie pola muszą być wypełnione!")
            return
        try:
            cena_float = float(cena.replace(",", "."))
            id_vat = lista_vat[idx_vat][0]
            id_kat = lista_kategorii[idx_kat][0]

            conn = pobierz_polaczenie()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO towar(nazwa, cena_netto, idstawki_vat, idkategoria) VALUES (%s, %s, %s, %s)",
                (nazwa, cena_float, id_vat, id_kat)
            )
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("OK", f"Towar '{nazwa}' został dodany!")
            okno_dodaj.destroy()
        except Exception as e:
            messagebox.showerror("Błąd bazy danych", f"Nie udało się zapisać danych:\n{e}")

    btn_zapisz = tk.Button(frame, text="Zapisz do bazy", command=zapisz_do_bazy)
    btn_zapisz.grid(row=4, column=0, columnspan=2, pady=20)

def dodaj_kategorie():
    okno_kat = tk.Toplevel(root)
    okno_kat.title("Dodaj kategorię")
    okno_kat.geometry("300x150")
    okno_kat.grab_set()

    frame = tk.Frame(okno_kat)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Nazwa kategorii:").grid(row=0, column=0, sticky=tk.W, pady=5)
    entry_nazwa = tk.Entry(frame, width=25)
    entry_nazwa.grid(row=0, column=1, pady=5)

    def zapisz_kategorie():
        nazwa = entry_nazwa.get().strip()
        if not nazwa:
            messagebox.showwarning("Błąd", "Podaj nazwę kategorii!")
            return
        try:
            conn = pobierz_polaczenie()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kategoria(nazwa) VALUES (%s)", (nazwa,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("OK", f"Kategoria '{nazwa}' dodana!")
            okno_kat.destroy()
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    btn_zapisz = tk.Button(frame, text="Zapisz", command=zapisz_kategorie)
    btn_zapisz.grid(row=1, column=0, columnspan=2, pady=10)

def dodaj_adres():
    okno_adr = tk.Toplevel(root)
    okno_adr.title("Dodaj adres klienta")
    okno_adr.geometry("350x300")
    okno_adr.grab_set()

    frame = tk.Frame(okno_adr)
    frame.pack(fill=tk.BOTH, expand=True)

    pola = ["Ulica:", "Numer:", "Kod pocztowy:", "Miejscowość:", "Województwo:"]
    entries = []
    for i, pole in enumerate(pola):
        tk.Label(frame, text=pole).grid(row=i, column=0, sticky=tk.W, pady=5)
        e = tk.Entry(frame, width=25)
        e.grid(row=i, column=1, pady=5)
        entries.append(e)

    def zapisz_adres():
        wartosci = [e.get().strip() for e in entries]
        if not all(wartosci):
            messagebox.showwarning("Błąd", "Wszystkie pola muszą być wypełnione!")
            return
        try:
            conn = pobierz_polaczenie()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO adres(ulica, numer, kod, miejscowosc, wojewodztwo) VALUES (%s, %s, %s, %s, %s)",
                wartosci
            )
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("OK", "Adres dodany!")
            okno_adr.destroy()
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    btn_zapisz = tk.Button(frame, text="Zapisz", command=zapisz_adres)
    btn_zapisz.grid(row=5, column=0, columnspan=2, pady=10)

root = tk.Tk()
root.title("Nasz sklep")
root.geometry("300x200")

label_info = tk.Label(root, text="Nasz sklep", font=("Arial", 12))
label_info.pack(pady=20)

btn_nowy_towar = tk.Button(root, text="Dodaj nowy towar (+)", command=dodaj_towar, bg="green", fg="white")
btn_nowy_towar.pack(pady=5)

btn_nowakat = tk.Button(root, text="Dodaj kategorię (+)", command=dodaj_kategorie, bg="green", fg="white")
btn_nowakat.pack(pady=0)

btn_adres = tk.Button(root, text="Dodaj adres klienta (+)", command=dodaj_adres, bg="blue", fg="white")
btn_adres.pack(pady=5)

root.mainloop()
