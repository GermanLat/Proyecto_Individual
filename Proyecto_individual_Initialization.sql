-- Para visualizar los usuarios que cargué a través del proyecto
SELECT * FROM users;
SELECT * FROM natural_persons;

-- Inicialización del tipo de transacciones (solo "Gastos" e "Ingresos" por ahora) (El nro de "id" específico se usa dentro del proyecto)
INSERT INTO transaction_types (name, created_at, updated_at) VALUES ("Gastos", NOW(), NOW());	-- 1: Gastos
INSERT INTO transaction_types (name, created_at, updated_at) VALUES ("Ingresos", NOW(), NOW());	-- 2: Ingresos
SELECT * FROM transaction_types;

-- Inicialización de categorías de transacciones bien básicas (El nro de "id" específico se usa dentro del proyecto)
INSERT INTO transaction_categories (name, transaction_type_id, created_at, updated_at) VALUES ("Gasto", 1, NOW(), NOW());
INSERT INTO transaction_categories (name, transaction_type_id, created_at, updated_at) VALUES ("Ingreso", 2, NOW(), NOW());
SELECT * FROM transaction_categories;

-- Corrección del "id" de las categorías de transacciones
UPDATE transaction_categories SET id=1, updated_at=NOW() WHERE id=3;	-- 1: Gasto
UPDATE transaction_categories SET id=2, updated_at=NOW() WHERE id=4;	-- 2: Ingreso

-- Ver transacciones
SELECT * FROM transactions;