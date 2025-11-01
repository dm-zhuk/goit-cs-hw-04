-- ********************************************
-- SQL-Запити для системи управління завданнями
-- ********************************************

-- Отримати всі завдання певного користувача
SELECT t.id, t.title, s.name AS status, u.fullname
FROM tasks t
JOIN status s ON t.status_id = s.id
JOIN users u ON t.user_id = u.id
WHERE t.user_id = 5;

-- Вибрати завдання за певним статусом ('new')
SELECT t.id, t.title, s.name AS status
FROM tasks t
JOIN status s ON t.status_id = s.id
WHERE s.name = 'new';


-- Оновити статус конкретного завдання
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 3;
    
-- Перевірка
SELECT title, (SELECT name FROM status WHERE id = status_id) FROM tasks WHERE id = 3;


-- Отримати список користувачів, які не мають жодного завдання
SELECT * FROM users
WHERE
    id NOT IN (
        SELECT DISTINCT user_id FROM tasks
    );


-- Додати нове завдання для конкретного користувача
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'Нове завдання (INSERT)',
    'Опис завдання, доданого через INSERT.',
    (SELECT id FROM status WHERE name = 'new'),
    2
);


-- Отримати всі завдання, які ще не завершено
SELECT t.id, t.title, s.name AS status
FROM tasks t
JOIN status s ON t.status_id = s.id
WHERE s.name != 'completed';


-- Видалити конкретне завдання
DELETE FROM tasks
WHERE id = 10;
    
-- Перевірка 
SELECT * FROM tasks WHERE id = 10;


-- Знайти користувачів з певною електронною поштою
SELECT fullname, email
FROM users
WHERE email LIKE '%@example.com';


-- Оновити ім'я користувача
UPDATE users
SET fullname = 'Tom Hardy'
WHERE id = 6;
    
-- Перевірка
SELECT * FROM users WHERE id = 6;


-- Отримати кількість завдань для кожного статусу
SELECT s.name AS status_name, COUNT(t.id) AS task_count
FROM status s
LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.name
ORDER BY task_count DESC;


-- Отримати завдання, які призначені користувачам з певною доменною частиною пошти
SELECT t.title, u.fullname, u.email
FROM tasks t 
JOIN users u ON t.user_id = u.id 
WHERE u.email LIKE '%@example.com';

-- Отримати список завдань, що не мають опису
SELECT id, title, description
FROM tasks
WHERE description IS NULL OR description = '';


-- Вибрати користувачів та їхні завдання у статусі 'in progress'
SELECT u.fullname, t.title, t.description 
FROM users u 
INNER JOIN tasks t ON u.id = t.user_id 
INNER JOIN status s ON t.status_id = s.id 
WHERE s.name = 'in progress';


-- Отримати користувачів та кількість їхніх завдань
SELECT u.fullname, COUNT(t.id) AS task_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id 
GROUP BY u.id, u.fullname
ORDER BY task_count DESC;