-- ============================================================
-- Sample data, loaded only the first time the database is created.
-- Default logins:
--   admin       / admin123   (role: admin)
--   coordinator / coord123   (role: coordinator)
-- Passwords are stored as SHA-256 hashes, never as plain text.
-- ============================================================

INSERT INTO users (username, password_hash, full_name, role) VALUES
('admin',       '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Cooperative Manager', 'admin'),
('coordinator', '8c63a2fc2b14d8ae6f9d0bf2e2c4227ac2dc4bd84768e1259226b0c3d84f1c65', 'Booking Coordinator', 'coordinator');

INSERT INTO guides (full_name, phone, gender, languages) VALUES
('Aline Uwera',      '0781234501', 'F', 'EN,FR'),
('Jean Bosco Habimana', '0781234502', 'M', 'EN,KIN'),
('Claudine Mukamana', '0781234503', 'F', 'FR,KIN,SW'),
('Eric Niyonzima',   '0781234504', 'M', 'EN,SW'),
('Diane Ingabire',   '0781234505', 'F', 'EN,FR,KIN');

INSERT INTO experiences (name, location, price_per_person, duration_hours) VALUES
('Village walk & banana beer making', 'Kinigi, Musanze',      30000, 3),
('Women artisans craft workshop',     'Musanze town',         25000, 2),
('Intore traditional dance evening',  'Kinigi, Musanze',      20000, 1.5),
('Coffee farm & roasting tour',       'Nyabihu',              35000, 4);

INSERT INTO bookings (tourist_name, group_size, tour_date, language, experience_id, guide_id, total_price, community_share, status, created_by) VALUES
('Sarah Miller',   2, '2026-11-10', 'EN', 1, 1, 60000, 6000, 'confirmed', 2),
('Luc Dubois',     3, '2026-11-12', 'FR', 2, 3, 75000, 7500, 'confirmed', 2),
('Amina Hassan',   1, '2026-11-15', 'SW', 4, 4, 35000, 3500, 'confirmed', 2),
('Tom Becker',     4, '2026-11-18', 'EN', 3, 2, 80000, 8000, 'cancelled', 2),
('Grace Kim',      2, '2026-11-20', 'EN', 1, 5, 60000, 6000, 'confirmed', 2),
('Paul Martin',    2, '2026-11-28', 'FR', 2, 1, 50000, 5000, 'confirmed', 2);
