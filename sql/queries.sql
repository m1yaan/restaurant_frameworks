-- 1. Все блюда по возрастанию цены
SELECT * FROM dishes ORDER BY price;
-- 2. Блюда выбранной категории
SELECT * FROM dishes WHERE category = 'Горячее';
-- 3. Клиенты
SELECT * FROM clients ORDER BY name;
-- 4. Заказы с именами клиентов
SELECT o.id, c.name, o.status FROM orders o JOIN clients c ON c.id=o.client_id;
-- 5. Заказы по столам
SELECT o.id, t.number FROM orders o JOIN restaurant_tables t ON t.id=o.table_id;
-- 6. Количество заказов по статусам
SELECT status, COUNT(*) FROM orders GROUP BY status;
-- 7. Состав заказа
SELECT oi.order_id, d.name, oi.quantity FROM order_items oi JOIN dishes d ON d.id=oi.dish_id;
-- 8. Стоимость каждого заказа
SELECT o.id, SUM(oi.quantity*d.price) total FROM orders o JOIN order_items oi ON oi.order_id=o.id JOIN dishes d ON d.id=oi.dish_id GROUP BY o.id;
-- 9. Средняя цена блюда
SELECT AVG(price) AS average_price FROM dishes;
-- 10. Самые популярные блюда
SELECT d.name, SUM(oi.quantity) sold FROM dishes d JOIN order_items oi ON oi.dish_id=d.id GROUP BY d.id ORDER BY sold DESC;
