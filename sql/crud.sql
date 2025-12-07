USE sto_test;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE order_parts;
TRUNCATE TABLE order_services;
TRUNCATE TABLE payments;
TRUNCATE TABLE invoices;
TRUNCATE TABLE orders;
TRUNCATE TABLE cars;
TRUNCATE TABLE mechanics;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO users (username, password, role)
VALUES 
('client1', '1234', 'client'),
('client2', '1234', 'client');

INSERT INTO mechanics (user_id, skill_level, experience_years) VALUES
((SELECT id FROM users WHERE username='mech1'), 'Електрика', 2),
((SELECT id FROM users WHERE username='mech2'), 'Двигун', 5),
((SELECT id FROM users WHERE username='mech3'), 'Гальмівна система', 3);

INSERT INTO cars (model, plate, owner_id) VALUES
('BMW 320', 'AA0011BB', (SELECT id FROM users WHERE username='client1')),
('Audi A6', 'AA2288CC', (SELECT id FROM users WHERE username='client1')),
('Toyota Camry', 'KA9912KK', (SELECT id FROM users WHERE username='client2'));

INSERT INTO orders (car_id, service_description, price, status, mechanic_notes, assigned_mechanic_id)
VALUES
((SELECT id FROM cars WHERE plate='AA0011BB'), 'Заміна масла та фільтра', 120.00, 'in_progress', 'Розпочав роботу', (SELECT id FROM users WHERE username='mech1')),
((SELECT id FROM cars WHERE plate='AA2288CC'), 'Ремонт гальмівної системи', 250.00, 'new', NULL, NULL),
((SELECT id FROM cars WHERE plate='KA9912KK'), 'Тюнінг двигуна', 400.00, 'done', 'Все зроблено якісно', (SELECT id FROM users WHERE username='mech2'));
INSERT INTO order_services (order_id, service_id)
VALUES
(1, 1),  
(2, 2),  
(3, 3);  

INSERT INTO order_parts (order_id, part_id)
VALUES
(1, 1),  
(2, 2);  

INSERT INTO invoices (order_id, total)
VALUES
(1, 120.00),
(2, 250.00),
(3, 400.00);

INSERT INTO payments (invoice_id, amount)
VALUES
(1, 120.00),
(3, 400.00);