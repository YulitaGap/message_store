-- CREATE DATABASE message_store_db;

CREATE TABLE authentication
(
	id serial PRIMARY KEY,
	login varchar(50) NOT NULL,
	password varchar(50) NOT NULL,
	author boolean NOT NULL
);

CREATE TABLE author
(
    id   integer PRIMARY KEY REFERENCES authentication(id),
    name varchar(50) NOT NULL,
	price_per_1000 numeric NOT NULL,
	active boolean NOT NULL
);

CREATE TABLE agent
(
    id   serial PRIMARY KEY,
    name varchar(50) NULL
);

CREATE TABLE author_agent
(
    group_id  integer REFERENCES agent (id),
    author_id integer REFERENCES author (id)
);

CREATE TABLE style
(
    id   serial      PRIMARY KEY,
    name varchar(50) NOT NULL
);

CREATE TABLE principal
(
    id   integer PRIMARY KEY REFERENCES authentication(id),
    name varchar(50) NOT NULL
);

CREATE TABLE social_network
(
    id   serial      PRIMARY KEY,
    name varchar(50) NOT NULL
);

CREATE TABLE account
(
    id           serial  PRIMARY KEY,
    principal_id integer REFERENCES principal (id),
    social_network_id integer REFERENCES social_network (id),
    login varchar(50) NOT NULL,
    password varchar(50) NOT NULL
);



CREATE TABLE discount
(
    id       serial  NOT NULL PRIMARY KEY,
    author_id integer NOT NULL REFERENCES author (id),
    style_id integer NOT NULL REFERENCES style (id),
    sale_to  date    NULL,
    discount numeric NULL
);

CREATE TABLE posts
(
    id         serial  PRIMARY KEY,
    account_id integer NOT NULL REFERENCES account (id),
    text       text    NOT NULL,
    style_id   integer NOT NULL REFERENCES style (id),
    date       date    NOT NULL,
    visible    boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE orders
(
    id           serial      NOT NULL PRIMARY KEY,
    principal_id integer     NOT NULL REFERENCES principal (id),
    agent_id     integer     NOT NULL REFERENCES agent (id),
    volume       integer     NOT NULL,
    post_id      integer     NOT NULL REFERENCES posts (id),
    price        numeric       NOT NULL,
    date         date        NOT NULL,
    status       varchar(50) NOT NULL
);
