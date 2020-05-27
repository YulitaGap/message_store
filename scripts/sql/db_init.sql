-- CREATE DATABASE message_store_db;

CREATE TABLE author
(
    id   serial PRIMARY KEY,
    name varchar(50) NOT NULL
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
    id   serial      PRIMARY KEY,
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
	social_network_id integer REFERENCES social_network (id)
);



CREATE TABLE discount
(
    id       serial  NOT NULL PRIMARY KEY,
    agent_id integer NOT NULL REFERENCES agent (id),
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
    date       date    NOT NULL
);

CREATE TABLE orders
(
    id           serial      NOT NULL PRIMARY KEY,
    principal_id integer     NOT NULL REFERENCES principal (id),
    agent_id     integer     NOT NULL REFERENCES agent (id),
    discount_id  integer     NULL     REFERENCES discount (id),
    post_id      integer     NOT NULL REFERENCES posts (id),
    price        money       NOT NULL,
    date         date        NOT NULL,
    status       varchar(50) NOT NULL
);
