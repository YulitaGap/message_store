#!/usr/bin/python3
from dataclasses import dataclass


@dataclass
class DBInfo:
    ip: str
    port: str
    db_name: str
    user: str
    paswd: str


db_auth = DBInfo("127.0.0.1", "5432", "message_store_db",
                 "postgres", "test")
