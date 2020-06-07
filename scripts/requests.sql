-- Request #2
select orders.principal_id, author.name, orders.date
from author
         inner join author_agent on author.id = author_agent.author_id
         inner join agent on author_agent.group_id = agent.id
         inner join orders on agent.id = orders.agent_id
where orders.principal_id = 1
  and orders.date > '2019-01-01'
  and orders.date < '2020-06-06';
-- Request #4
select principal_id, count(id)
from orders
where date > '2019-01-01'
  and date < '2020-06-06'
group by principal_id
having count(id) > 0;
-- Request #6
select author.name, account.id, account.social_network_id, orders.date
from author
         inner join author_agent on author.id = author_agent.author_id
         inner join agent on author_agent.group_id = agent.id
         inner join orders on agent.id = orders.agent_id
         inner join principal on orders.principal_id = principal.id
         inner join account on principal.id = account.principal_id
where orders.date > '2019-01-01'
  and orders.date < '2020-06-06';
-- Request #8
select author.id,
       author.name,
       orders.date       as order_date,
       case
           when access_history.give_access = TRUE then access_history.date
           else null end as allowed_access,
       case
           when access_history.give_access = FALSE then access_history.date
           else null end as denied_access,
       discount.sale_to
from orders
         inner join posts on orders.id = posts.id
         inner join style on posts.style_id = style.id
         inner join discount on style.id = discount.style_id
         inner join agent on orders.principal_id = agent.id
         inner join author_agent on agent.id = author_agent.group_id
         inner join author on author_agent.author_id = author.id
         inner join access_history on agent.id = access_history.agent_id
where author.id = 31
  and orders.principal_id = 1
  and ((access_history.date between d1 and d2) or
       (orders.date between d1 and d2) or
       (discount.sale_to between d1 and d2)
    or (allowed_access between d1 and d2));
-- Request #10
select orders.principal_id, style.name, count(orders.id)
from orders
         inner join posts on orders.post_id = posts.id
         inner join style on posts.style_id = style.id
         inner join discount on style.id = discount.style_id
where principal_id = 1
  and discount = 0.9
  and orders.date between d1 and d2
group by style.name, orders.principal_id;
-- Request #12
select max(social_network.name)              as s,
       style.name,
       count(*) / count(distinct style.name) as counter
from social_network
         inner join account on social_network.id = account.social_network_id
         inner join posts on account.id = posts.account_id
         inner join style on posts.style_id = style.id
         inner join discount on style.id = discount.style_id
         inner join author on discount.author_id = author.id
where author.id = 33
  and posts.date between '2000-01-01' and '2020-08-12'
group by style.name
order by s;
