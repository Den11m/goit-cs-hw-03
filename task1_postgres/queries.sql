-- SQL Queries for Task Management System
-- Example values (user_id = 1, task_id = 1, domain 'example.com', ...) can be changed as needed

-- Query 1: Get all tasks for a specific user by user_id
SELECT * FROM tasks WHERE user_id = 1;

-- Query 2: Get tasks with a specific status using subquery
SELECT * FROM tasks
WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- Query 3: Change status of a specific task to 'in progress'
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 1;

-- Query 4: Find users who have no tasks using WHERE NOT IN and subquery
SELECT * FROM users
WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks WHERE user_id IS NOT NULL);

-- Query 5: Add a new task for a specific user
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('New Task Title', 'Task description',
        (SELECT id FROM status WHERE name = 'new'),
        1);

-- Query 6: Get all incomplete tasks (not 'completed')
SELECT t.*, s.name AS status_name
FROM tasks t
JOIN status s ON t.status_id = s.id
WHERE s.name != 'completed';

-- Query 7: Delete a task by its id
DELETE FROM tasks WHERE id = 2;

-- Query 8: Find users by email using LIKE
SELECT * FROM users WHERE email LIKE '%@example.com';

-- Query 9: Update user name
UPDATE users SET fullname = 'John Doe' WHERE id = 1;

-- Query 10: Count tasks for each status using COUNT and GROUP BY
SELECT s.name AS status_name, COUNT(t.id) AS task_count
FROM status s
LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.id, s.name
ORDER BY s.id;

-- Query 11: Get tasks of users with a specific email domain using JOIN and LIKE
SELECT t.*, u.email
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.com';

-- Query 12: Find tasks without description
SELECT * FROM tasks WHERE description IS NULL OR description = '';

-- Query 13: Get users and their tasks with status 'in progress' using INNER JOIN
SELECT u.fullname, u.email, t.title, t.description
FROM users u
INNER JOIN tasks t ON u.id = t.user_id
INNER JOIN status s ON t.status_id = s.id
WHERE s.name = 'in progress';

-- Query 14: Get users and count of their tasks using LEFT JOIN and GROUP BY
SELECT u.id, u.fullname, u.email, COUNT(t.id) AS task_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id, u.fullname, u.email
ORDER BY task_count DESC;
