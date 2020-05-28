-- Here should be code for queries due to the task
--1
Select author.name, principal.name, count(orders.principal_id)
FROM author
INNER JOIN author_agent ON id = author_id
INNER JOIN agent ON author_agent.group_id = agent.id
INNER JOIN orders ON agent.id = orders.agent_id
INNER JOIN principal ON orders.principal_id = principal.id
GROUP BY author.id ,author.name, principal.name, orders.date
HAVING author.id = 4 AND count(orders.principal_id) > 0 AND orders.date >'2020-05-20' AND  orders.date <'2020-06-05'
--3
SELECT author.name, count(author.name)
FROM author
INNER JOIN author_agent ON id = author_id
INNER JOIN agent ON author_agent.group_id = agent.id
INNER JOIN orders ON agent.id = orders.agent_id
INNER JOIN principal ON orders.principal_id = principal.id
GROUP BY author.name, orders.date
HAVING count(author.name) > 0 AND orders.date >'2020-05-20' AND  orders.date <'2020-06-05'
--5
SELECT principal.name, social_network.name
FROM principal
INNER JOIN orders ON orders.principal_id = principal.id
INNER JOIN account ON principal.id = account.principal_id
INNER JOIN social_network ON social_network.id = account.social_network_id
GROUP BY social_network.name, orders.principal_id, principal.id
HAVING principal.id = 3 AND count(orders.principal_id) > 0
