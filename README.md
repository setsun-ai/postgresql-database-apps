# PostgreSQL database design and Tkinter client apps

Relational database design in PostgreSQL plus small desktop clients built with Python, Tkinter and psycopg2.
MSc student project, Gdańsk University of Technology, 2026. Course: *Data Sets and Their Protection*.

## Hotel reservation database (`hotel_project/`)

- **Normalised schema:** room types and prices, rooms, equipment (M:N), clients, reservations.
- **Integrity:** primary and foreign keys, `UNIQUE` constraints, and a `CHECK` that departure is after arrival.
- **View:** `v_rezerwacje` joins all tables and computes the number of nights and the total price.
- **Docs:** ER diagram (`er_diagram.pdf`) and project documentation.

```bash
psql -d hotel -f hotel_project/hotel_schema.sql
```

## Shop database with GUI clients (`shop_db/`)

- **SQL exercises:**
  - inserts with constraint tests
  - views joining clients and addresses
- **Tkinter apps** (psycopg2):
  - add products, with category and VAT dropdowns read from the DB
  - browse tables in a grid
  - client list
  - simple shop front-end

Connection settings come from the standard PostgreSQL environment variables:

```bash
export PGHOST=localhost PGDATABASE=sklep PGUSER=postgres PGPASSWORD=...
python shop_db/apps/dodaj_towar.py
```

**Data:** all names, e-mails and phone numbers in the SQL scripts are made-up sample data. The original database ran on a university lab server; credentials and the server address have been removed from the code.

**Tools:** PostgreSQL, SQL (DDL/DML, views, constraints), Python, Tkinter, psycopg2.

## AI assistance

The code in this repository was written with the help of AI tools (large language models). Defining the tasks, running the analyses, and checking and interpreting the results were my part of the work.

---

## 🇵🇱 Opis po polsku

Projekt bazy danych hotelu (schemat, więzy integralności, widok rezerwacji, diagram ER) oraz aplikacje w Tkinterze do bazy sklepu (dodawanie towarów, przeglądanie tabel, lista klientów). Dane logowania do bazy są pobierane ze zmiennych środowiskowych.

Projekt studencki (studia II stopnia), Politechnika Gdańska, 2026.

**Wsparcie AI:** kod w tym repozytorium powstał z pomocą narzędzi AI (dużych modeli językowych). Określenie zadań, uruchamianie analiz oraz sprawdzenie i interpretacja wyników były moją częścią pracy.
