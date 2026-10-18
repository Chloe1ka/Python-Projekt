INSERT INTO mitglied (vorname, nachname, email) VALUES
    ('Lina', 'Berg', 'lina.berg@example.com'),
    ('Omar', 'Kaya', 'omar.kaya@example.com');

INSERT INTO vertrag (mitglied_id, tarif, beginn) VALUES
    (1, 'Monat', '2026-01-01'),
    (2, 'Jahr', '2026-02-01');

INSERT INTO checkin (mitglied_id, zeitpunkt) VALUES
    (1, '2026-10-01 08:15'),
    (1, '2026-10-03 18:40'),
    (1, '2026-10-05 09:05'),
    (2, '2026-10-02 17:00');
