-- Скидаємо базу, якщо існує
DROP DATABASE IF EXISTS sto_test;
CREATE DATABASE sto_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sto_test;

-- Таблиця користувачів
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(80) NOT NULL UNIQUE,
  password VARCHAR(200) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'client'
);

-- Таблиця автомобілів
CREATE TABLE cars (
  id INT AUTO_INCREMENT PRIMARY KEY,
  model VARCHAR(120) NOT NULL,
  plate VARCHAR(30) NOT NULL,
  owner_id INT NOT NULL,
  FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Таблиця замовлень
CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  car_id INT NOT NULL,
  service_description VARCHAR(500) NOT NULL,
  price DECIMAL(10,2) NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'new',
  mechanic_notes VARCHAR(500) NULL,
  assigned_mechanic_id INT NULL,
  FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE,
  FOREIGN KEY (assigned_mechanic_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Таблиця сервісів
CREATE TABLE services (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(500) NULL
);

-- Проміжна таблиця orders <-> services
CREATE TABLE order_services (
  order_id INT NOT NULL,
  service_id INT NOT NULL,
  PRIMARY KEY (order_id, service_id),
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
);

-- Таблиця рахунків
CREATE TABLE invoices (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- Таблиця платежів
CREATE TABLE payments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  invoice_id INT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  paid_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
);

-- Таблиця запчастин
CREATE TABLE parts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  price DECIMAL(10,2) NOT NULL
);

-- Проміжна таблиця orders <-> parts
CREATE TABLE order_parts (
  order_id INT NOT NULL,
  part_id INT NOT NULL,
  PRIMARY KEY (order_id, part_id),
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY (part_id) REFERENCES parts(id) ON DELETE CASCADE
);

-- Додаткові дані для сервісів та запчастин
INSERT INTO services (name, description) VALUES 
('Заміна масла', 'Заміна моторного масла та фільтра'),
('Ремонт гальм', 'Перевірка та заміна гальмівних колодок'),
('Тюнінг двигуна', 'Поліпшення потужності двигуна');

INSERT INTO parts (name, price) VALUES
('Фільтр масляний', 15.00),
('Гальмівні колодки', 50.00);
