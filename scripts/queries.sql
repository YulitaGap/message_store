-- Here should be code for queries due to the task
--1
SELECT author.name, principal.name, count(orders.principal_id)
FROM author
         INNER JOIN author_agent ON id = author_id
         INNER JOIN agent ON author_agent.group_id = agent.id
         INNER JOIN orders ON agent.id = orders.agent_id
         INNER JOIN principal ON orders.principal_id = principal.id
GROUP BY author.id, author.name, principal.name, orders.date
HAVING author.id = 4
   AND count(orders.principal_id) > 0
   AND orders.date > '2020-05-20'
   AND orders.date < '2020-06-05';
--3
SELECT foo.name
FROM (SELECT author.name, principal.id
      FROM author
               INNER JOIN author_agent ON id = author_id
               INNER JOIN agent ON author_agent.group_id = agent.id
               INNER JOIN orders ON agent.id = orders.agent_id
               INNER JOIN principal ON orders.principal_id = principal.id
      GROUP BY author.name, orders.date, principal.id
      HAVING count(author.name) > 0
         AND orders.date > '2020-05-20'
         AND orders.date < '2020-06-05') as foo
Group By foo.name
Having count(foo.name) > 1;
--5
SELECT principal.name, social_network.name
FROM principal
         INNER JOIN orders ON orders.principal_id = principal.id
         INNER JOIN account ON principal.id = account.principal_id
         INNER JOIN social_network
                    ON social_network.id = account.social_network_id
GROUP BY social_network.name, orders.principal_id, principal.id, orders.date
HAVING principal.id = 3
   AND count(orders.principal_id) > 0
   AND orders.date > '2020-05-20'
   AND orders.date < '2020-06-05';
--9
Select (author.name)
From (Select author_agent.group_id, count(author_agent.group_id)
      FROM author
               INNER JOIN author_agent ON id = author_id
               INNER JOIN agent ON author_agent.group_id = agent.id
               INNER JOIN orders ON agent.id = orders.agent_id
               INNER JOIN principal ON orders.principal_id = principal.id
               INNER JOIN account ON account.principal_id = principal.id
               INNER JOIN social_network
                          ON account.principal_id = social_network.id
      GROUP BY social_network.id, author_agent.group_id, orders.date
      HAVING count(social_network.id) > 2
         AND orders.date > '2020-05-20'
         AND orders.date < '2020-06-05') AS foo
         Inner Join agent ON agent.id = foo.group_id
         INNER JOIN author_agent ON agent.id = author_agent.group_id
         INNER JOIN author ON author.id = author_agent.author_id
WHERE author.name = 'Nelia';

--11
SELECT count(month), foo.month
FROM (SELECT (CASE
                  WHEN EXTRACT(MONTH FROM orders.date) = 5 THEN
                      'May'
                  WHEN EXTRACT(MONTH FROM orders.date) = 6 THEN
                      'June'
                  WHEN EXTRACT(MONTH FROM orders.date) = 7 THEN
                      'July'
                  WHEN EXTRACT(MONTH FROM orders.date) = 8 THEN
                      'August'
                  WHEN EXTRACT(MONTH FROM orders.date) = 9 THEN
                      'September'
                  WHEN EXTRACT(MONTH FROM orders.date) = 10 THEN
                      'October'
                  WHEN EXTRACT(MONTH FROM orders.date) = 11 THEN
                      'November'
                  WHEN EXTRACT(MONTH FROM orders.date) = 12 THEN
                      'December'
                  WHEN EXTRACT(MONTH FROM orders.date) = 4 THEN
                      'April'
                  WHEN EXTRACT(MONTH FROM orders.date) = 3 THEN
                      'March'
                  WHEN EXTRACT(MONTH FROM orders.date) = 2 THEN
                      'February'
                  ELSE
                      'January'
    END) AS month
      FROM orders) AS foo
GROUP BY foo.month;
--7
SELECT author.name
FROM principal
         INNER JOIN account ON principal.id = account.principal_id
         INNER JOIN access_history ON access_history.account_id = account.id
         INNER JOIN agent ON agent.id = access_history.agent_id
         INNER JOIN author_agent ON agent.id = author_agent.group_id
         INNER JOIN author ON author.id = author_agent.author_id
GROUP BY author.name, access_history.agent_id, principal.id, principal.name
HAVING count(author.name) = 2
   AND principal.name = 'Laurie';
