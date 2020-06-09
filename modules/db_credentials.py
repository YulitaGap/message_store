#!/usr/bin/python3
class DBInfo:
    def __init__(self, ip, port, db_name, user, paswd):
        self.ip: str = ip
        self.port: str = port
        self.db_name: str = db_name
        self.user: str = user
        self.paswd: str = paswd


db_auth = DBInfo("127.0.0.1", "5432", "message_store_db",
                 "postgres", "test")
