#!/usr/bin/python3
from flask_restful import Resource

"""
The REST API documentation is at 'docs/rest_api.txt'
"""

_STATUS_FOUND = 302
_STATUS_OK = 200
_STATUS_INVALID_PARAMETERS = 400


class BaseApiEndpoint(Resource):
    @staticmethod
    def data_base_query(query):
        return {}


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

    def get(self):
        """
        Params:
            client_id=<client id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
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

    def get(self):
        """
        Params:
            client_id=<client id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(ClientUsedAuthors.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(PopularAuthors.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(ActiveClients.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            client_id=<client id>(int)
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(ClientActiveNetworks.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(RatedAuthorsDistinctClients.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(PopularClients.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            order_threshold=<min order num of author>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(ClientsPopularNetworks.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            author_id=<author id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(AuthorUsedAccounts.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            client_id=<client id>(int)
        """
        return self.data_base_query(ClientsTrustedAuthors.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            client_id=<client id>(int)
            author_id=<author id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(ClientUserRelations.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            author_id=<author id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(AuthorTeamWorksByNetwork.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            client_id=<client id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(ClientsHalfDiscountsByStyle.SQL_QUERY), \
               _STATUS_FOUND


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
        return self.data_base_query(OrdersCountByMonths.SQL_QUERY), \
               _STATUS_FOUND


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

    def get(self):
        """
        Params:
            author_id=<author id>(int)
            begin_date=<begin of search period>(yyyy-mm-dd)
            end_date=<end of search period>(yyyy-mm-dd)
        """
        return self.data_base_query(AuthorsOrderedTopNetworks.SQL_QUERY), \
               _STATUS_FOUND


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
