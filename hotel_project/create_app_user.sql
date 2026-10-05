-- Least-privilege application role for the hotel database.
-- Run as the database owner AFTER hotel_schema.sql, e.g.:
--   psql -d hotel -f hotel_project/create_app_user.sql
-- then set the password interactively (it is never stored in a file):
--   psql -d hotel -c "\password hotel_app"

CREATE ROLE hotel_app LOGIN;

REVOKE ALL ON DATABASE hotel FROM PUBLIC;
GRANT CONNECT ON DATABASE hotel TO hotel_app;
GRANT USAGE ON SCHEMA public TO hotel_app;

-- Reference data: read only.
GRANT SELECT ON typ_pokoju, pokoj, element_wyposazenia, wyposazenie_pokoju TO hotel_app;

-- Day-to-day operations: guests and reservations can be added and updated, not deleted.
GRANT SELECT, INSERT, UPDATE ON klient_hotel, rezerwacja TO hotel_app;
GRANT USAGE ON SEQUENCE klient_hotel_klient_id_seq, rezerwacja_rezerwacja_id_seq TO hotel_app;

-- Reporting view.
GRANT SELECT ON v_rezerwacje TO hotel_app;
