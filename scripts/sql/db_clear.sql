-- clear from all content

TRUNCATE orders, access_history, posts, discount, account, style, author_agent,
    agent, author, principal, social_network, authentication RESTART IDENTITY CASCADE;
