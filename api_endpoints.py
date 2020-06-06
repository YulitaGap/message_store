#!/usr/bin/python3
from flask_restful import Resource, reqparse
import sql_builder as sb

"""
The REST API documentation is at 'docs/rest_api.txt'
"""

_STATUS_FOUND = 302
_STATUS_OK = 200
_STATUS_INVALID_PARAMETERS = 400


class BaseApiEndpoint(Resource):
    @staticmethod
    def data_base_query(query: str) -> dict:
        return {}

    @staticmethod
    def is_valid_date(date: str) -> bool:
        return True

    @staticmethod
    def not_null(*args) -> bool:
        return True


class ConstantClients(BaseApiEndpoint):
    """
    Action:
        client_used_authors
    Desc:
        Для покупця С знайти усiх авторiв, у яких вiн замовляв повiдомлення
        чи статтi за вказаний перiод (з дати F по дату T);
    """
    SQL_QUERY = ""
    ROUTE = "/constant_clients"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            client_id=<client id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = ConstantClients.PARSER.parse_args(strict=True)
        return self.data_base_query(ConstantClients.SQL_QUERY), \
               _STATUS_FOUND


class ClientUsedAuthors(BaseApiEndpoint):
    """
    Action:
        client_used_authors
    Desc:
        Для покупця С знайти усiх авторiв, у яких вiн замовляв повiдомлення
        чи статтi за вказаний перiод (з дати F по дату T)
    """
    SQL_QUERY = ""
    ROUTE = "/client_used_authors"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            client_id=<client id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = ClientUsedAuthors.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(ClientUsedAuthors.SQL_QUERY), \
        #        _STATUS_FOUND


class PopularAuthors(BaseApiEndpoint):
    """
    Action:
        popular_authors
    Desc:
        Знайти усiх авторiв, якi отримували замовлення вiд щонайменше N рiзних
        покупцiв за вказаний перiод (з дати F по дату T)
    """
    SQL_QUERY = ""
    ROUTE = "/popular_authors"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = PopularAuthors.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(PopularAuthors.SQL_QUERY), \
        #        _STATUS_FOUND


class ActiveClients(BaseApiEndpoint):
    """
    Action:
        active_clients
    Desc:
        Знайти усiх покупцiв, якi зробили хоча б N замовлень за вказаний перiод
        (з дати F по дату T)
    """
    SQL_QUERY = ""
    ROUTE = "/active_clients"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = ActiveClients.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(ActiveClients.SQL_QUERY), \
        #        _STATUS_FOUND


class ClientActiveNetworks(BaseApiEndpoint):
    """
    Action:
        client_active_networks
    Desc:
        Для покупця С знайти усi соцiальнi мережi, для яких вiн зробив хоча б N
        замовлень за вказаний перiод (з дати F по дату T)
    """
    SQL_QUERY = ""
    ROUTE = "/client_active_networks"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            client_id=<client id>(int)
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = ClientActiveNetworks.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(ClientActiveNetworks.SQL_QUERY), \
        #        _STATUS_FOUND


class RatedAuthorsDistinctClients(BaseApiEndpoint):
    """
    Action:
        rated_authors_distinct_clients
    Desc:
        Знайти усiх авторiв, якi отримували замовлення вiд щонайменше N рiзних
        покупцiв за вказаний перiод (з дати F по дату T)
    """
    SQL_QUERY = ""
    ROUTE = "/rated_authors_distinct_clients"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = RatedAuthorsDistinctClients.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(RatedAuthorsDistinctClients.SQL_QUERY), \
        #        _STATUS_FOUND


class PopularClients(BaseApiEndpoint):
    """
    Action:
        popular_clients
    Desc:
        Знайти усiх покупцiв, якi зробили хоча б N замовлень за вказаний перiод
        (з дати F по дату T)
    """
    SQL_QUERY = ""
    ROUTE = "/popular_clients"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = PopularClients.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(PopularClients.SQL_QUERY), \
        #        _STATUS_FOUND


class ClientsPopularNetworks(BaseApiEndpoint):
    """
    Action:
        clients_popular_networks
    Desc:
        Для покупця С знайти усi соцiальнi мережi, для яких вiн зробив хоча б N
        замовлень за вказаний перiод (з дати F по дату T)
    """
    SQL_QUERY = ""
    ROUTE = "/clients_popular_networks"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('order_threshold', type=int,
                        help='min order num of author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            client_id=<client id>(int)
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = ClientsPopularNetworks.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(ClientsPopularNetworks.SQL_QUERY), \
        #        _STATUS_FOUND


class AuthorUsedAccounts(BaseApiEndpoint):
    """
    Action:
        author_used_accounts
    Desc:
        Для автора А знайти усi облiковi записи у соцiальних мережах, до яких вiн
        мав доступ протягом вказаного перiоду (з дати F по дату T)
    """
    SQL_QUERY = ""
    ROUTE = "/author_used_accounts"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            author_id=<author id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = AuthorUsedAccounts.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(AuthorUsedAccounts.SQL_QUERY), \
        #        _STATUS_FOUND


class ClientsTrustedAuthors(BaseApiEndpoint):
    """
    Action:
        clients_trusted_authors
    Desc:
        Для покупця С знайти усiх авторiв, яким вiн надав доступ до хоча б одного
        облiкового запису у соцiальнiй мережi, а потiм позбавив його цього доступу.
    """
    SQL_QUERY = ""
    ROUTE = "/clients_trusted_authors"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')

    def get(self):
        """
        Params:
            client_id=<client id>(int)
        """
        args = ClientsTrustedAuthors.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(ClientsTrustedAuthors.SQL_QUERY), \
        #        _STATUS_FOUND


class ClientUserRelations(BaseApiEndpoint):
    """
    Action:
        client_user_relations
    Desc:
        Знайти усi спiльнi подiї для автора A та покупця С за вказаний перiод
        (з дати F по дату T)
    """
    SQL_QUERY = ""
    ROUTE = "/client_user_relations"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            client_id=<client id>(int)
            author_id=<author id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = ClientUserRelations.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(ClientUserRelations.SQL_QUERY), \
        #        _STATUS_FOUND


class AuthorTeamWorksByNetwork(BaseApiEndpoint):
    """
    Action:
            author_team_works_by_network
        Desc:
            Для автора A та кожної соцiальної мережi, у якiй вiн писав статтю, знайти
            скiльки разiв за вказаний перiод (з дати F по дату T) вiн писав її у групi
            з щонайменше N авторiв.
    """
    SQL_QUERY = ""
    ROUTE = "/author_team_works_by_network"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            author_id=<author id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = AuthorTeamWorksByNetwork.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(AuthorTeamWorksByNetwork.SQL_QUERY), \
        #        _STATUS_FOUND


class ClientsHalfDiscountsByStyle(BaseApiEndpoint):
    """
    Action:
        clients_half_discounts_by_style
    Desc:
        Для покупця С та кожного стилю, у якому вiн замовляв повiдомлення, знайти
        скiльки замовлень за вказаний перiод (з дати F по дату T) отримали 50%
        знижку.
    """
    SQL_QUERY = ""
    ROUTE = "/clients_half_discounts_by_style"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('client_id', type=int, help='id of the client')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            client_id=<client id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = ClientsHalfDiscountsByStyle.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(ClientsHalfDiscountsByStyle.SQL_QUERY), \
        #        _STATUS_FOUND


class OrdersCountByMonths(BaseApiEndpoint):
    """
    Action:
        orders_count_by_months
    Desc:
        Знайти сумарну кiлькiсть замовлень по мiсяцях.
    """
    SQL_QUERY = ""
    ROUTE = "/orders_count_by_months"

    def get(self):
        """
        No params
        """
        args = OrdersCountByMonths.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(OrdersCountByMonths.SQL_QUERY), \
        #        _STATUS_FOUND


class AuthorsOrderedTopNetworks(BaseApiEndpoint):
    """
    Action:
        authors_ordered_top_networks
    Desc:
        Вивести соцiальнi мережi у порядку спадання середньої кiлькостi повiдомлень
        по усiх стилях, що були написанi автором A за вказаний перiод
        (з дати F по дату T).
    """
    SQL_QUERY = ""
    ROUTE = "/authors_ordered_top_networks"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('author_id', type=int, help='id of the author')
    PARSER.add_argument('begin_date', type=str, help='begin of search period')
    PARSER.add_argument('end_date', type=str, help='end of search period')

    def get(self):
        """
        Params:
            author_id=<author id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        args = AuthorsOrderedTopNetworks.PARSER.parse_args(strict=True)
        return args
        # return self.data_base_query(AuthorsOrderedTopNetworks.SQL_QUERY), \
        #        _STATUS_FOUND


class CreateOrder(BaseApiEndpoint):
    # TODO: Check everything here and add to ENDPOINTS_LIST
    """
    Action:
        create_order
    Desc:
        Перевіряє чи з даним набором авторів є агент і повертає його ід або нічого,
        якщо нічого, то створює агента з таким набором авторів і повертає його ід.
    """
    ROUTE = "/create_order"
    PARSER = reqparse.RequestParser()
    PARSER.add_argument('account_id', type=int, help='id of the account')
    PARSER.add_argument('principal_id', type=int, help='id of the principal')
    PARSER.add_argument('author_id', type=list, help='ids of the author')
    PARSER.add_argument('style_id', type=int, help='id of the style')
    PARSER.add_argument('volume', type=int, help='number of symbols')

    def get(self):
        args = AuthorsOrderedTopNetworks.PARSER.parse_args(strict=True)
        agent_id = self.data_base_query(sb.find_agent(args['author_id']))['id']
        if len(agent_id.values()) == 0:
            agent_id = self.data_base_query(sb.create_agent(args['author_id']))['id']
        price = self.data_base_query(sb.get_price(args['author_id'], args['style_id']))['price_per_1000']
        return self.data_base_query(sb.create_order(args['account_id'],
                                                    args['principal_id'],
                                                    agent_id,
                                                    args['style_id'],
                                                    price,
                                                    args['volume']))
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
