#!/usr/bin/python3
import psycopg2
from flask_restful import Resource, reqparse, abort

from modules import sql_builder as sb

"""
The REST API documentation is at 'docs/rest_api.txt'
"""

_STATUS_FOUND = 302
_STATUS_OK = 200
_STATUS_INVALID_PARAMETERS = 400


def connect_to_db(func):
    def res_func(query):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="postgres",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="message_store")

            # ################## OUTER FUNCTION  ###################
            return func(query, connection)
            # ######################################################

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while accessing PostgresSQL Data Base!", error)
            abort(_STATUS_INVALID_PARAMETERS)
        finally:
            # closing database connection.
            if connection:
                connection.close()

    return res_func


class BaseApiEndpoint(Resource):
    @staticmethod
    @connect_to_db
    def data_base_select_query(query: str, connection=None) -> dict:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()

    @staticmethod
    @connect_to_db
    def data_base_updating_query(query: str, connection=None) -> dict:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            return {}
        finally:
            cursor.close()

    # TODO Виідалити це і написати нормально (або змиритися)
    @staticmethod
    @connect_to_db
    def data_base_update_select_query(query: str, connection=None) -> dict:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return result
        finally:
            cursor.close()

    def get(self):
        a = self.PARSER.parse_args(strict=True)
        return self.data_base_select_query(
            self.SQL_QUERY(a)), _STATUS_FOUND


class ConstantClients(BaseApiEndpoint):
    """
    Request #1
    Action:
        contant_clients
    Desc:
        для автора A знайти усiх покупцiв, якi замовляли у нього повiдомлення
        хоча б N разiв за вказаний перiод (з дати F по дату T);
    """
    SQL_QUERY = lambda _self, params: \
        f"""
    SELECT DISTINCT principal.name
    FROM author
             INNER JOIN author_agent ON id = author_id
             INNER JOIN agent ON author_agent.group_id = agent.id
             INNER JOIN orders ON agent.id = orders.agent_id
             INNER JOIN principal ON orders.principal_id = principal.id
    WHERE author.id = {params['author_id']}
    AND orders.date >= date('{params['begin_date']}')
    AND orders.date <= date('{params['end_date']}')
    GROUP BY author.name, principal.name
    HAVING count(orders.principal_id) >= {params['limit']} ;
    """
    ROUTE = "/constant_clients"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')
    PARSER.add_argument('limit', type=int, help='upper limit')


class ClientUsedAuthors(BaseApiEndpoint):
    """
    Request #2
    Action:
        client_used_authors
    Desc:
        Для покупця С знайти усiх авторiв, у яких вiн замовляв повiдомлення
        чи статтi за вказаний перiод (з дати F по дату T)
        
    """
    SQL_QUERY = lambda _self, params: \
        f"""
    select author.name, text(orders.date) from author
    inner join author_agent on author.id = author_agent.author_id
    inner join agent on author_agent.group_id = agent.id
    inner join orders on agent.id = orders.agent_id
    where orders.principal_id = {params['client_id']}
    and orders.date >= date('{params['begin_date']}')
    and orders.date <= date('{params['end_date']}');
    """
    ROUTE = "/client_used_authors"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class PopularAuthors(BaseApiEndpoint):
    """
    Request #3
    Action:
        popular_authors
    Desc:
        Знайти усiх авторiв, якi отримували замовлення вiд щонайменше N рiзних
        покупцiв за вказаний перiод (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: \
        f"""
    SELECT foo.name
    FROM (SELECT author.name
          FROM author
                   INNER JOIN author_agent ON id = author_id
                   INNER JOIN agent ON author_agent.group_id = agent.id
                   INNER JOIN orders ON agent.id = orders.agent_id
                   INNER JOIN principal ON orders.principal_id = principal.id
          WHERE orders.date > date('{params['begin_date']}')
              AND orders.date < date('{params['end_date']}')
          GROUP BY author.name, principal.id
          HAVING count(author.name) > 0) as foo
    GROUP BY foo.name
    HAVING count(foo.name) > {params['order_threshold']};
    """
    ROUTE = "/popular_authors"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class ActiveClients(BaseApiEndpoint):
    """
    Request #4
    Action:
        active_clients
    Desc:
        Знайти усiх покупцiв, якi зробили хоча б N замовлень за вказаний перiод
        (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: f"""
    select principal.name, s.count from principal
    inner join
    (
    select principal_id, count(id) from orders 
    where date between date('{params['begin_date']}') and date('{params['end_date']}')
    group by principal_id
    having count(id) >= {params['order_threshold']}) as s
    on principal.id = s.principal_id
    """
    ROUTE = "/active_clients"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class ClientActiveNetworks(BaseApiEndpoint):
    """
    Request #5
    Action:
        client_active_networks
    Desc:
        Для покупця С знайти усi соцiальнi мережi, для яких вiн зробив хоча б N
        замовлень за вказаний перiод (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: \
        f"""
    SELECT principal.name, social_network.name
    FROM principal
             INNER JOIN orders ON orders.principal_id = principal.id
             INNER JOIN account ON principal.id = account.principal_id
             INNER JOIN social_network
                        ON social_network.id = account.social_network_id
    WHERE orders.date >= date('{params['begin_date']}')
       AND orders.date <= date('{params['end_date']}')
    GROUP BY social_network.name, orders.principal_id, principal.id
    HAVING principal.id = {params['client_id']} 
       AND count(orders.principal_id) >= {params['order_threshold']};
    """
    ROUTE = "/client_active_networks"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class AuthorUsedAccounts(BaseApiEndpoint):
    """
    Request #6
    Action:
        author_used_accounts
    Desc:
        Для автора А знайти усi облiковi записи у соцiальних мережах, до яких
        вiн мав доступ протягом вказаного перiоду (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: f"""
    select author.name, access_history.account_id, access_history.give_access,
    text(access_history.date) as date from access_history
    inner join author_agent on access_history.agent_id = author_agent.group_id
    inner join author on (author.id = author_agent.author_id)
    where author.id = {params['author_id']}
    and access_history.date >= date('{params['begin_date']}')
    and access_history.date <= date('{params['end_date']}') 
    """
    ROUTE = "/author_used_accounts"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class ClientsTrustedAuthors(BaseApiEndpoint):
    """
    Request #7
    Action:
        clients_trusted_authors
    Desc:
        Для покупця С знайти усiх авторiв, яким вiн надав доступ до хоча б
        одного облiкового запису у соцiальнiй мережi, а потiм позбавив його
        цього доступу.
    """
    SQL_QUERY = lambda _self, params: f"""
    select author.name from 
    (select distinct account_id, agent_id from access_history
    where give_access = true
    intersect
    select distinct account_id, agent_id from access_history
    where give_access = false) as s
    inner join author_agent on (author_agent.group_id = s.agent_id)
    inner join author on (author.id = author_agent.author_id)
    inner join account on (account.id = s.account_id)
    where account.principal_id = {params['client_id']};
    """
    ROUTE = "/clients_trusted_authors"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')


class ClientUserRelations(BaseApiEndpoint):
    """
    Request #8
    Action:
        client_user_relations
    Desc:
        Знайти усi спiльнi подiї для автора A та покупця С за вказаний перiод
        (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: f"""
    select author.id, author.name, orders.date as order_date, 
        case when access_history.give_access = TRUE then access_history.date else null end as allowed_access,
        case when access_history.give_access = FALSE then access_history.date else null end as denied_access,
        discount.sale_to
    from orders
    inner join posts on orders.id = posts.id
    inner join style on posts.style_id = style.id
    inner join discount on style.id = discount.style_id
    inner join agent on orders.principal_id = agent.id
    inner join author_agent on agent.id = author_agent.group_id
    inner join author on author_agent.author_id = author.id
    inner join access_history on agent.id = access_history.agent_id
    where author.id = {params['author_id']} and orders.principal_id = {params['client_id']} and 
    ((access_history.date between {params['begin_date']} and {params['end_date']}) or 
     (orders.date between {params['begin_date']} and {params['end_date']}) or 
     (discount.sale_to between {params['begin_date']} and {params['end_date']}) 
     or (allowed_access between {params['begin_date']} and {params['end_date']}));
    """
    ROUTE = "/client_user_relations"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class AuthorTeamWorksByNetwork(BaseApiEndpoint):
    """
    Request #9
    Action:
            author_team_works_by_network
        Desc:
            Для автора A та кожної соцiальної мережi, у якiй вiн писав статтю,
            знайти скiльки разiв за вказаний перiод (з дати F по дату T) вiн
            писав її у групi з щонайменше N авторiв.
    """
    SQL_QUERY = lambda _self, params: f"""
    SELECT count(author.name)
    FROM (SELECT author_agent.group_id, count(author_agent.group_id)
          FROM author
                   INNER JOIN author_agent ON id = author_id
                   INNER JOIN agent ON author_agent.group_id = agent.id
                   INNER JOIN orders ON agent.id = orders.agent_id
                   INNER JOIN principal ON orders.principal_id = principal.id
                   INNER JOIN account ON account.principal_id = principal.id
                   INNER JOIN social_network
                              ON account.principal_id = social_network.id
          WHERE orders.date
               > date('{params['begin_date']}')
             AND orders.date
               < date('{params['end_date']}')
          GROUP BY social_network.id, author_agent.group_id
          HAVING count(social_network.id) > {params['limit']}) AS foo
             INNER JOIN agent ON agent.id = foo.group_id
             INNER JOIN author_agent ON agent.id = author_agent.group_id
             INNER JOIN author ON author.id = author_agent.author_id
    WHERE author.id = {params['author_id']}
    GROUP BY author.name;
    """
    ROUTE = "/author_team_works_by_network"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')
    PARSER.add_argument('limit', type=str, help='limit of authors')


class ClientsHalfDiscountsByStyle(BaseApiEndpoint):
    """
    Request #10
    Action:
        clients_half_discounts_by_style
    Desc:
        Для покупця С та кожного стилю, у якому вiн замовляв повiдомлення,
        знайти скiльки замовлень за вказаний перiод (з дати F по дату T)
        отримали 50% знижку.
    """
    SQL_QUERY = lambda _self, params: f"""
    select orders.principal_id as client, style.name as style, count(orders.id) from orders
    inner join posts on orders.post_id = posts.id
    inner join style on posts.style_id = style.id
    inner join discount on style.id = discount.style_id
    where principal_id = {params['client_id']} and discount = 0.5
    and orders.date between date('{params['begin_date']}') and date('{params['end_date']}')
    group by style.name, orders.principal_id;
    """
    ROUTE = "/clients_half_discounts_by_style"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class OrdersCountByMonths(BaseApiEndpoint):
    """
    Request #11
    Action:
        orders_count_by_months
    Desc:
        Знайти сумарну кiлькiсть замовлень по мiсяцях.
    """
    SQL_QUERY = lambda _self, params: f"""
    SELECT count(month), foo.month
    FROM
    (SELECT
    (CASE 
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
    """
    ROUTE = "/orders_count_by_months"
    PARSER = reqparse.RequestParser()


class AuthorsOrderedTopNetworks(BaseApiEndpoint):
    """
    Request #12
    Action:
        authors_ordered_top_networks
    Desc:
        Вивести соцiальнi мережi у порядку спадання середньої кiлькостi
        повiдомлень по усiх стилях, що були написанi автором A за вказаний
        перiод (з дати F по дату T).
    """
    SQL_QUERY = lambda _self, params: f"""
    select a.s as network, a.b as style_id, round(cast(avg(a.countr) as numeric(12,2)), 2) as freq from
    (select social_network.name as s, posts.style_id as b, count(orders.id) as countr from social_network
    inner join account on social_network.id = account.social_network_id
    inner join posts on account.id = posts.account_id
    inner join orders on posts.id = orders.post_id
    inner join agent on orders.agent_id = agent.id
    inner join author_agent on agent.id = author_agent.group_id
    inner join author on author_agent.author_id = author.id
    where author.id = {params['author_id']} and posts.date between {params['begin_date']} and {params['end_date']}
    group by posts.style_id, s
    order by countr desc) a
    group by a.s, a.b;
    """
    ROUTE = "/authors_ordered_top_networks"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class CreateOrder(BaseApiEndpoint):
    """
    Action:
        create_order
    Desc:
        Перевіряє чи з даним набором авторів є агент і повертає його ід або
        нічого, якщо нічого, то створює агента з таким набором авторів і
        повертає його ід.
    """
    SQL_QUERY = lambda _self, params: ""
    ROUTE = "/create_order"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('account_id', type=int, help='id of the account')
    PARSER.add_argument('principal_id', type=int, help='id of the principal')
    PARSER.add_argument('author_id', type=str, help='ids of the author')
    PARSER.add_argument('style_id', type=int, help='id of the style')
    PARSER.add_argument('volume', type=int, help='number of symbols')

    def get(self):
        args = self.PARSER.parse_args(strict=True)
        args['author_id'] = [int(i) for i in str(args['author_id']).split(",")]
        agent_id = self.data_base_select_query(
            sb.find_agent(args['author_id']))
        if len(agent_id) == 0:
            agent_id = self.data_base_update_select_query(
                sb.create_agent(args['author_id']))

        price = self.data_base_select_query(
            sb.get_price(args['author_id'],
                         args['style_id']))

        return self.data_base_updating_query(
            sb.create_order(args['account_id'], args['principal_id'],
                            agent_id[0][0], args['style_id'], float(price[0][0]), args['volume'])), _STATUS_FOUND


class AddAccount(BaseApiEndpoint):
    """
    Action:
        add_account
    Desc:
        Покупець додає аккаунт у соц.мережі.
    """
    ROUTE = "/add_account"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('principal_id', type=int, help='id of the client')
    PARSER.add_argument('social_network_id', type=int, help='id of the social network')
    PARSER.add_argument('login', type=str, help='client login')
    PARSER.add_argument('password', type=str, help='client password')

    def get(self):
        args = self.PARSER.parse_args(strict=True)
        self.data_base_updating_query(sb.create_account(args['principal_id'], args['social_network_id'], args['login'],
                                                        args['password']))


class ViewAuthors(BaseApiEndpoint):
    """
    Action:
        view_authors
    Desc:
        Покупець переглядає перелік доступних авторів.
    """
    SQL_QUERY = """
    select id, name, text(price_per_1000) from author
    where active is TRUE;
    """
    ROUTE = "/view_authors"

    def get(self):
        return self.data_base_select_query(self.SQL_QUERY)


class ViewStyles(BaseApiEndpoint):
    """
    Action:
        view_styles
    Desc:
        Покупець переглядає перелік стилів для замовлення.
    """
    SQL_QUERY = """
    select * from style
    """
    ROUTE = "/view_styles"

    def get(self):
        return self.data_base_select_query(self.SQL_QUERY), _STATUS_FOUND


class ViewUserOrders(BaseApiEndpoint):
    """
    Action:
        view_user_orders
    Desc:
        Покупець переглядає перелік своїх відкритих замовлень.
    """
    SQL_QUERY = lambda _self, params: \
        f"""
        select orders.id, orders.agent_id,
        text(orders.price), text(orders.date),
        orders.volume, orders.post_id, orders.status
        from orders
        where principal_id = {params['client_id']} and status != 'closed';
        """
    ROUTE = "/view_user_orders"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')

    def get(self):
        args = self.PARSER.parse_args(strict=True)
        return self.data_base_select_query(self.SQL_QUERY(args)), _STATUS_FOUND


class UpdateUserOrder(BaseApiEndpoint):
    """
    Action:
        update_user_order
    Desc:
        Покупець змінює статус замовлення.
    """
    SQL_QUERY = lambda _self, params: \
        f"""
        update orders set status = '{params['status']}' where id = {params['order_id']} ;
        """
    ROUTE = "/update_user_order"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('order_id', type=int, help='id of the order')
    PARSER.add_argument('status', type=str, help='new status')

    def get(self):
        args = self.PARSER.parse_args(strict=True)
        return self.data_base_updating_query(self.SQL_QUERY(args)), _STATUS_FOUND


class ViewUserPost(BaseApiEndpoint):
    """
    Action:
        view_user_post
    Desc:
        Покупець переглядає наповнення та стан поста.
    """
    SQL_QUERY = lambda _self, params: \
        f"""
        select orders.id, posts.text, posts.style_id from posts
        inner join orders on posts.id = orders.post_id
        where orders.principal_id = {params['principal_id']} and orders.status != 'closed'
        """
    PARSER = reqparse.RequestParser()
    ROUTE = "/view_user_post"
    PARSER.add_argument('principal_id', type=int, help='id of the principal')

    def get(self):
        args = self.PARSER.parse_args(strict=True)
        return self.data_base_select_query(self.SQL_QUERY(args)), \
               _STATUS_FOUND


class UpdateUserPost(BaseApiEndpoint):
    """
    Action:
        update_user_post
    Desc:
        Покупець змінює стан поста.
    """
    SQL_QUERY = lambda _self, params: \
        f"""
        UPDATE posts SET visible = TRUE WHERE id = {params['post_id']}
        """
    PARSER = reqparse.RequestParser()
    ROUTE = "/update_user_post"
    PARSER.add_argument('post_id', type=int, help='id of the post')

    def get(self):
        args = self.PARSER.parse_args(strict=True)
        return self.data_base_updating_query(self.SQL_QUERY(args)), \
               _STATUS_FOUND


class GiveAccess(BaseApiEndpoint):
    """
    Action:
        give_access
    Desc:
        Дати або забрати доступ
    """
    SQL_QUERY = lambda _self, params: \
        f""" INSERT INTO access_history(agent_id, account_id, give_access, date)
VALUES ({params['agent_id']}, {params['account_id']}, {params['give']}, CURRENT_DATE)
        """
    PARSER = reqparse.RequestParser()
    ROUTE = "/give_access"
    PARSER.add_argument('agent_id', type=int, help='id of the post')
    PARSER.add_argument('account_id', type=int, help='id of the post')
    PARSER.add_argument('give', type=str, help='id of the post')

    def get(self):
        args = self.PARSER.parse_args(strict=True)
        return self.data_base_updating_query(self.SQL_QUERY(args)), \
               _STATUS_FOUND


ENDPOINTS_LIST = [
    ConstantClients,
    ClientUsedAuthors,
    PopularAuthors,
    ActiveClients,
    ClientActiveNetworks,
    AuthorUsedAccounts,
    ClientsTrustedAuthors,
    AuthorTeamWorksByNetwork,
    ClientsHalfDiscountsByStyle,
    OrdersCountByMonths,
    AuthorsOrderedTopNetworks,
    CreateOrder,
    AddAccount,
    ViewAuthors,
    ViewStyles,
    ViewUserOrders,
    UpdateUserOrder,
    ViewUserPost,
    UpdateUserPost,
    GiveAccess
]
