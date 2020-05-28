-- Request #2
select orders.principal_id, author.name, orders.date from author
inner join author_agent on author.id = author_agent.author_id
inner join agent on author_agent.group_id = agent.id
inner join orders on agent.id = orders.agent_id
where orders.principal_id = 1 and orders.date > '2019-01-01' and orders.date < '2020-06-06';
-- Request #4
select principal_id, count(id) from orders 
where date > '2019-01-01' and date < '2020-06-06'
group by principal_id
having count(id) > 0;
-- Request #6
select author.name, account.id, account.social_network_id, orders.date from author
inner join author_agent on author.id = author_agent.author_id
inner join agent on author_agent.group_id = agent.id
inner join orders on agent.id = orders.agent_id
inner join principal on orders.principal_id = principal.id
inner join account on principal.id = account.principal_id
where orders.date > '2019-01-01' and orders.date < '2020-06-06'; 
-- Request #8
-- Request #10
-- Request #12
