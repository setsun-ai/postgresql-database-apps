CREATE VIEW klienci_z_adresami AS
SELECT k.klient_id, k.imie, k.nazwisko, k.telefon, k.email,
       a.ulica, a.numer, a.kod, a.miejscowosc, a.wojewodztwo
FROM klient k
JOIN klient_adres ka ON k.klient_id = ka.idkli
JOIN adres a ON ka.idard = a.adres_id;

SELECT * FROM klienci_z_adresami;





cd lab3
nano towary.txt

Kolba 250ml	25	23	2
Kolba 500ml	35	23	2
Zlewka 100ml	8	23	6
Zlewka 250ml	12	23	6
Zlewka 500ml	18	23	6
Kuweta 1cm	22	23	5
Kuweta 2cm	28	23	5
Pipeta 5ml	15	23	4
Pipeta 20ml	32	23	4
Probówka 10ml	6	23	1

\copy towar(nazwa,cena_netto,vat,idkategoria) from lab3/towary.txt

SELECT * FROM towar;



INSERT INTO klient(imie, nazwisko, nazwa_firmy, telefon, email) VALUES
('Piotr', 'Zalewski', 'PZ Lab', '000000003', 'pz@example.com'),
('Kasia', 'Wrobel', 'BioTech', '000000004', 'kw@example.com');

INSERT INTO adres(ulica, numer, kod, miejscowosc, wojewodztwo) VALUES
('Morska', '5', '81-323', 'Gdynia', 'pomorskie'),
('Dluga', '10', '80-828', 'Gdansk', 'pomorskie');

INSERT INTO klient_adres VALUES
(8,7),(9,8);

INSERT INTO faktura(data, klientid) VALUES
('2026-05-10', 8),
('2026-05-15', 9),
('2026-05-20', 1);

INSERT INTO zakup(towar_id, faktura_id, ilosc) VALUES
(11, 4, 2),(12, 4, 3),(13, 4, 1),
(14, 5, 5),(15, 5, 2),(16, 5, 4),
(11, 6, 1),(13, 6, 3),(14, 6, 2);

SELECT k.imie, k.nazwisko, f.numer, f.data
FROM klient k
JOIN faktura f ON f.klientid = k.klient_id;