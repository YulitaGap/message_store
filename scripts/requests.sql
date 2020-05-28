-- Request #2
-- для покупця С знайти усiх авторiв, 
-- у яких вiн замовляв повiдомлення чи статтi за вказаний
-- перiод (з дати F по дату T);

select principal_id, date, author_id from orders
inner join (select * from author_agent
inner join author on author_agent.author_id = author.id) A
on orders.agent_id = A.group_id
where principal_id = 1 and date > '2019-01-01' and date < '2020-06-06';

-- Request #4
-- знайти усiх покупцiв, якi зробили хоча б
-- N замовлень за вказаний перiод 
-- (з дати F по дату T);

select principal_id, count(id) as coun from orders 
where date > '2019-01-01' and date < '2020-06-06'
group by principal_id
having count(id) > 0;

-- Request #6
-- для автора А знайти усi облiковi записи 
-- у соцiальних мережах, до яких вiн мав доступ
-- протягом вказаного перiоду (з дати F по дату T);

-- select * from 
-- (select * from account
-- inner join orders
-- on account.principal_id = orders.principal_id) as A
-- inner join 
-- (select * from author_agent
--  inner join author 
--  on author_agent.author_id = author.id) as B
--  on A.agent_id;

-- Request #8
-- знайти усi спiльнi подiї для автора A
-- та покупця С за вказаний перiод (з дати F по дату
-- T);

