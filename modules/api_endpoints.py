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
                                          password="test",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="message_store_db")

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

    def get(self):
        a = self.PARSER.parse_args(strict=True)
        return self.data_base_select_query(
            self.SQL_QUERY(a)), _STATUS_FOUND


class ConstantClients(BaseApiEndpoint):
    """
    Action:
        contant_clients
    Desc:
        для автора A знайти усiх покупцiв, якi замовляли у нього повiдомлення
        хоча б N разiв за вказаний перiод (з дати F по дату T);
    """
    SQL_QUERY = lambda _self, params: \
        f"""
    SELECT author.name, principal.name, count(orders.principal_id)
    FROM author
             INNER JOIN author_agent ON id = author_id
             INNER JOIN agent ON author_agent.group_id = agent.id
             INNER JOIN orders ON agent.id = orders.agent_id
             INNER JOIN principal ON orders.principal_id = principal.id
    GROUP BY author.id, author.name, principal.name, orders.date
    HAVING author.id = 4
       AND count(orders.principal_id) > {params['limit']} 
       AND orders.date > date({params['begin_date']})
       AND orders.date < date({params['end_date']});
    """
    ROUTE = "/constant_clients"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')
    PARSER.add_argument('limit', type=int, help='upper limit')


class ClientUsedAuthors(BaseApiEndpoint):
    """
    Action:
        client_used_authors
    Desc:
        Для покупця С знайти усiх авторiв, у яких вiн замовляв повiдомлення
        чи статтi за вказаний перiод (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: ""
    ROUTE = "/client_used_authors"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class PopularAuthors(BaseApiEndpoint):
    """
    Action:
        popular_authors
    Desc:
        Знайти усiх авторiв, якi отримували замовлення вiд щонайменше N рiзних
        покупцiв за вказаний перiод (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: \
        f"""
    SELECT foo.name
    FROM (SELECT author.name,
          FROM author
                   INNER JOIN author_agent ON id = author_id
                   INNER JOIN agent ON author_agent.group_id = agent.id
                   INNER JOIN orders ON agent.id = orders.agent_id
                   INNER JOIN principal ON orders.principal_id = principal.id
          GROUP BY author.name, orders.date, principal.id
          HAVING count(author.name) > 0
             AND orders.date > date({params['begin_date']})
             AND orders.date < date({params['end_date']})) as foo
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
    Action:
        active_clients
    Desc:
        Знайти усiх покупцiв, якi зробили хоча б N замовлень за вказаний перiод
        (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: ""
    ROUTE = "/active_clients"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class ClientActiveNetworks(BaseApiEndpoint):
    """
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
    GROUP BY social_network.name, orders.principal_id, principal.id
    HAVING principal.id = {params['client_id']} 
       AND count(orders.principal_id) > {params['order_threshold']}
       AND orders.date > date({params['begin_date']})
       AND orders.date < date({params['end_date']});
    """
    ROUTE = "/client_active_networks"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class RatedAuthorsDistinctClients(BaseApiEndpoint):
    """
    Action:
        rated_authors_distinct_clients
    Desc:
        Знайти усiх авторiв, якi отримували замовлення вiд щонайменше N рiзних
        покупцiв за вказаний перiод (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: ""
    ROUTE = "/rated_authors_distinct_clients"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class PopularClients(BaseApiEndpoint):
    """
    Action:
        popular_clients
    Desc:
        Знайти усiх покупцiв, якi зробили хоча б N замовлень за вказаний перiод
        (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: ""
    ROUTE = "/popular_clients"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class ClientsPopularNetworks(BaseApiEndpoint):
    """
    Action:
        clients_popular_networks
    Desc:
        Для покупця С знайти усi соцiальнi мережi, для яких вiн зробив хоча б N
        замовлень за вказаний перiод (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: ""
    ROUTE = "/clients_popular_networks"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class AuthorUsedAccounts(BaseApiEndpoint):
    """
    Action:
        author_used_accounts
    Desc:
        Для автора А знайти усi облiковi записи у соцiальних мережах, до яких
        вiн мав доступ протягом вказаного перiоду (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: ""
    ROUTE = "/author_used_accounts"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class ClientsTrustedAuthors(BaseApiEndpoint):
    """
    Action:
        clients_trusted_authors
    Desc:
        Для покупця С знайти усiх авторiв, яким вiн надав доступ до хоча б
        одного облiкового запису у соцiальнiй мережi, а потiм позбавив його
        цього доступу.
    """
    SQL_QUERY = lambda _self, params: f"""
    SELECT author.name
    FROM principal
             INNER JOIN account ON principal.id = account.principal_id
             INNER JOIN access_history ON 
                                         access_history.account_id = account.id
             INNER JOIN agent ON agent.id = access_history.agent_id
             INNER JOIN author_agent ON agent.id = author_agent.group_id
             INNER JOIN author ON author.id = author_agent.author_id
    GROUP BY author.name, access_history.agent_id, principal.id
    HAVING count(author.name) = 2
       AND principal.id = {params['client_id']};
    """
    ROUTE = "/clients_trusted_authors"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')


class ClientUserRelations(BaseApiEndpoint):
    """
    Action:
        client_user_relations
    Desc:
        Знайти усi спiльнi подiї для автора A та покупця С за вказаний перiод
        (з дати F по дату T)
    """
    SQL_QUERY = lambda _self, params: ""
    ROUTE = "/client_user_relations"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class AuthorTeamWorksByNetwork(BaseApiEndpoint):
    """
    Action:
            author_team_works_by_network
        Desc:
            Для автора A та кожної соцiальної мережi, у якiй вiн писав статтю,
            знайти скiльки разiв за вказаний перiод (з дати F по дату T) вiн
            писав її у групi з щонайменше N авторiв.
    """
    SQL_QUERY = lambda _self, params: f"""
    SELECT (author.name)
    FROM (SELECT author_agent.group_id, count(author_agent.group_id)
          FROM author
                   INNER JOIN author_agent ON id = author_id
                   INNER JOIN agent ON author_agent.group_id = agent.id
                   INNER JOIN orders ON agent.id = orders.agent_id
                   INNER JOIN principal ON orders.principal_id = principal.id
                   INNER JOIN account ON account.principal_id = principal.id
                   INNER JOIN social_network
                              ON account.principal_id = social_network.id
          GROUP BY social_network.id, author_agent.group_id, orders.date
          HAVING count(social_network.id) > {params['limit']}
             AND orders.date
               > date({params['begin_date']})
             AND orders.date
               < date({params['end_date']})) AS foo
             INNER JOIN agent ON agent.id = foo.group_id
             INNER JOIN author_agent ON agent.id = author_agent.group_id
             INNER JOIN author ON author.id = author_agent.author_id
    WHERE author.id = {params['author_id']};
    """
    ROUTE = "/author_team_works_by_network"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')
    PARSER.add_argument('limit', type=str, help='limit of authors')


class ClientsHalfDiscountsByStyle(BaseApiEndpoint):
    """
    Action:
        clients_half_discounts_by_style
    Desc:
        Для покупця С та кожного стилю, у якому вiн замовляв повiдомлення,
        знайти скiльки замовлень за вказаний перiод (з дати F по дату T)
        отримали 50% знижку.
    """
    SQL_QUERY = lambda _self, params: ""
    ROUTE = "/clients_half_discounts_by_style"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class OrdersCountByMonths(BaseApiEndpoint):
    """
    Action:
        orders_count_by_months
    Desc:
        Знайти сумарну кiлькiсть замовлень по мiсяцях.
    """
    SQL_QUERY = lambda _self, params: f"""
    SELECT count(num)
    FROM (SELECT count(orders.id) as num
          FROM orders
          GROUP BY orders.id
          WHERE orders.date > date({params['begin_date']}) 
             AND orders.date < date({params['end_date']})) AS foo
    GROUP BY num;
    """
    ROUTE = "/orders_count_by_months"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class AuthorsOrderedTopNetworks(BaseApiEndpoint):
    """
    Action:
        authors_ordered_top_networks
    Desc:
        Вивести соцiальнi мережi у порядку спадання середньої кiлькостi
        повiдомлень по усiх стилях, що були написанi автором A за вказаний
        перiод (з дати F по дату T).
    """
    SQL_QUERY = lambda _self, params: ""
    ROUTE = "/authors_ordered_top_networks"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')


class CreateOrder(BaseApiEndpoint):
    # TODO: Check everything here and add to ENDPOINTS_LIST
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
    PARSER.add_argument('author_id', type=list, help='ids of the author')
    PARSER.add_argument('style_id', type=int, help='id of the style')
    PARSER.add_argument('volume', type=int, help='number of symbols')

    def get(self):
        args = AuthorsOrderedTopNetworks.PARSER.parse_args(strict=True)
        agent_id = self.data_base_select_query(
            sb.find_agent(args['author_id']))['id']
        if len(agent_id.values()) == 0:
            agent_id = self.data_base_select_query(
                sb.create_agent(args['author_id']))['id']

        price = self.data_base_select_query(
            sb.get_price(args['author_id'],
                         args['style_id']))['price_per_1000']

        return self.data_base_select_query(
            sb.create_order(args['account_id'], args['principal_id'],
                            agent_id, args['style_id'], price, args['volume']))
        # , \
        #        _STATUS_FOUND


ENDPOINTS_LIST = [
    ConstantClients,
    ClientUsedAuthors,
    PopularAuthors,
    ActiveClients,
    ClientActiveNetworks,
    RatedAuthorsDistinctClients,
    PopularClients,
    ClientsPopularNetworks,
    AuthorUsedAccounts,
    ClientsTrustedAuthors,
    AuthorTeamWorksByNetwork,
    ClientsHalfDiscountsByStyle,
    OrdersCountByMonths,
    AuthorsOrderedTopNetworks
]
