CREATE TABLE typ_pokoju (
    typ_id    serial PRIMARY KEY,
    nazwa     varchar(50) NOT NULL,
    cena_doba money NOT NULL
);

CREATE TABLE pokoj (
    pokoj_id  serial PRIMARY KEY,
    numer     varchar(10) NOT NULL UNIQUE,
    pietro    smallint NOT NULL DEFAULT 0,
    idtypu    int NOT NULL REFERENCES typ_pokoju
);

CREATE TABLE element_wyposazenia (
    element_id serial PRIMARY KEY,
    nazwa      varchar(100) NOT NULL
);

CREATE TABLE wyposazenie_pokoju (
    idpokoju  int NOT NULL REFERENCES pokoj,
    idelement int NOT NULL REFERENCES element_wyposazenia,
    ilosc     int NOT NULL DEFAULT 1,
    PRIMARY KEY (idpokoju, idelement)
);

CREATE TABLE klient_hotel (
    klient_id serial PRIMARY KEY,
    imie      varchar(50) NOT NULL,
    nazwisko  varchar(50) NOT NULL,
    email     varchar(100),
    telefon   varchar(20),
    pesel     char(11) UNIQUE,
    nr_dowodu varchar(20) UNIQUE
);

CREATE TABLE rezerwacja (
    rezerwacja_id   serial PRIMARY KEY,
    idklienta       int NOT NULL REFERENCES klient_hotel,
    idpokoju        int NOT NULL REFERENCES pokoj,
    data_przyjazdu  date NOT NULL,
    data_wyjazdu    date NOT NULL,
    status          varchar(20) NOT NULL DEFAULT 'oczekujaca',
    data_rezerwacji timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_daty CHECK (data_wyjazdu > data_przyjazdu)
);

CREATE VIEW v_rezerwacje AS
SELECT
    r.rezerwacja_id,
    k.imie,
    k.nazwisko,
    p.numer AS numer_pokoju,
    t.nazwa AS typ_pokoju,
    r.data_przyjazdu,
    r.data_wyjazdu,
    (r.data_wyjazdu - r.data_przyjazdu) AS liczba_dob,
    t.cena_doba,
    t.cena_doba * (r.data_wyjazdu - r.data_przyjazdu) AS kwota_total,
    r.status
FROM rezerwacja r
JOIN klient_hotel k ON r.idklienta = k.klient_id
JOIN pokoj p ON r.idpokoju = p.pokoj_id
JOIN typ_pokoju t ON p.idtypu = t.typ_id;

INSERT INTO typ_pokoju(nazwa, cena_doba) VALUES
('Jednoosobowy', 150.00),
('Dwuosobowy', 220.00),
('Apartament', 450.00);

INSERT INTO pokoj(numer, pietro, idtypu) VALUES
('101', 1, 1),
('102', 1, 1),
('201', 2, 2),
('202', 2, 2),
('301', 3, 3);

INSERT INTO element_wyposazenia(nazwa) VALUES
('Telewizor'),
('Klimatyzacja'),
('Łóżko jednoosobowe'),
('Łóżko dwuosobowe'),
('Mini-bar'),
('Sejf');

INSERT INTO wyposazenie_pokoju(idpokoju, idelement, ilosc) VALUES
(1, 1, 1), (1, 3, 1),
(2, 1, 1), (2, 3, 1),
(3, 1, 1), (3, 2, 1), (3, 4, 1),
(4, 1, 1), (4, 2, 1), (4, 4, 1),
(5, 1, 1), (5, 2, 1), (5, 4, 1), (5, 5, 1), (5, 6, 1);

INSERT INTO klient_hotel(imie, nazwisko, email, telefon) VALUES
('Anna', 'Kowalska', 'anna.k@example.com', '000-000-001'),
('Tomasz', 'Wiśniewski', 't.wisniewski@example.com', '000-000-002');

INSERT INTO rezerwacja(idklienta, idpokoju, data_przyjazdu, data_wyjazdu, status) VALUES
(1, 3, '2026-06-01', '2026-06-05', 'potwierdzona'),
(2, 5, '2026-06-10', '2026-06-12', 'oczekujaca');

SELECT * FROM v_rezerwacje;