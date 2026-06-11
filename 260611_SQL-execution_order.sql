SELECT
    c.customer_name,
    COUNT(o.order_id)  AS total_orders,
    SUM(o.amount)      AS total_spent
FROM   
    customers c
JOIN   
    orders o        
    ON c.customer_id = o.customer_id
WHERE  
    o.order_date  >= '2024-01-01'
GROUP BY 
    c.customer_id, c.customer_name
HAVING 
    SUM(o.amount)  > 500
ORDER BY 
    total_spent  DESC
LIMIT 10;