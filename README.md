# PostgreSQL database design and Tkinter client apps

**MSc coursework.** A normalised PostgreSQL schema for hotel reservations, with integrity constraints, a reporting view and a least-privilege application role. It also includes small Tkinter + psycopg2 desktop clients for a course shop database.

## Context & motivation

Life-science and chemistry projects end up storing samples, measurements and metadata. A well-designed relational schema keeps that data consistent through keys, constraints and views instead of ad-hoc spreadsheets. The course (*Data Sets and Their Protection*) covered:
- data models (flat, hierarchical/XML, JSON, relational),
- SQL in PostgreSQL,
- basic data protection: integrity, access control, keeping credentials out of code.

This repository applies them to a small but complete example: a hotel booking database that you can build from scratch.

## Hotel reservation database (`hotel_project/`)

- **Normalised schema:** room types and prices, rooms, equipment (M:N via `wyposazenie_pokoju`), clients, reservations.
- **Integrity:** primary and foreign keys, `UNIQUE` on room numbers and ID-document fields, and `CHECK (data_wyjazdu > data_przyjazdu)`.
- **View:** `v_rezerwacje` joins all tables and computes the number of nights and the total price.
- **Access control:** [`create_app_user.sql`](hotel_project/create_app_user.sql) creates a `hotel_app` login role:
  - read-only on reference data,
  - `SELECT/INSERT/UPDATE` (no `DELETE`) on guests and reservations,
  - no access to anything else.
- **Docs:** ER diagram ([`er_diagram.pdf`](hotel_project/er_diagram.pdf)) and project documentation (Polish).

### Run from scratch

```bash
createdb hotel
psql -d hotel -f hotel_project/hotel_schema.sql      # tables, constraints, view, sample data
psql -d hotel -f hotel_project/create_app_user.sql   # least-privilege role
psql -d hotel -c "\password hotel_app"               # set its password interactively
psql -d hotel -U hotel_app -c "SELECT * FROM v_rezerwacje;"
```

Both SQL files parse with the PostgreSQL grammar (checked with `pglast`).

## Shop database clients (`shop_db/`)

- **SQL exercises:** inserts with constraint tests, views joining clients and addresses.
- **Tkinter apps (psycopg2):**
  - adding products, with category and VAT dropdowns read from the database,
  - browsing tables in a grid,
  - a client list,
  - a simple shop front-end.

The base tables of the shop database (`towar`, `kategoria`, `klient`, …) were provided by the course lab server and are not part of this repository. These apps document the exercise and cannot be run from scratch without that schema.

## Configuration and credentials

Connection settings come from the standard PostgreSQL variables (`PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`). See [`.env.example`](.env.example).
- **Password:** the apps ask for it interactively (`getpass` or a masked dialog), or libpq reads it from `~/.pgpass`. It is never stored in code.
- **Removed from the original code:** the university server address and a hard-coded password.

```bash
export PGHOST=localhost PGDATABASE=hotel PGUSER=hotel_app
python shop_db/apps/dodaj_towar.py
```

## Repository structure

```
hotel_project/   schema + sample data, least-privilege role, ER diagram, documentation
shop_db/sql/     lab SQL exercises (inserts, constraints, views)
shop_db/apps/    Tkinter + psycopg2 clients
.env.example     connection settings template (no secrets)
```

## Data

All names, e-mails and phone numbers in the SQL scripts are made-up sample data. E-mails use `example.com` and phone numbers are dummies.

## Scope

- **Set by the course:**
  - the shop lab database and its exercises,
  - the requirement to design and document a relational database (ER diagram, DDL, sample data),
  - client applications in Python.
- **My decisions:**
  - the hotel domain and its schema,
  - the constraints and the reporting view,
  - the least-privilege role and the credential handling in this repository.

## AI usage

AI-assisted development was used for implementation and documentation. Method choice, validation strategy, data-handling decisions, result verification and interpretation were reviewed and owned by me.

## License

MIT (see [LICENSE](LICENSE)).

---

## 🇵🇱 Opis po polsku

Projekt z przedmiotu *Zbiory danych i ich ochrona* (kierunek InfoBioChem, studia II stopnia, Politechnika Gdańska, 2026).

- **Baza hotelu:** znormalizowany schemat, więzy integralności (klucze, `UNIQUE`, `CHECK` dat), widok rezerwacji i diagram ER. Bazę da się postawić od zera komendami z sekcji *Run from scratch*.
- **Rola o minimalnych uprawnieniach:** `hotel_app` ma tylko odczyt danych słownikowych oraz dodawanie i edycję gości i rezerwacji, bez usuwania.
- **Aplikacje Tkinter do bazy sklepu:** tabele bazowe sklepu pochodziły z serwera laboratoryjnego i nie ma ich w repozytorium.
- **Hasła:** podawane interaktywnie lub przez `~/.pgpass`, nigdy w kodzie.

**Wsparcie AI:** kod i dokumentacja powstały z pomocą narzędzi AI. Projekt bazy, decyzje dotyczące danych i weryfikacja należały do mnie.
