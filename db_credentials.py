#!/usr/bin/python3
from dataclasses import dataclass


@dataclass
class DBInfo:
    ip: str
    port: str
    db_name: str
    user: str
    paswd: str
