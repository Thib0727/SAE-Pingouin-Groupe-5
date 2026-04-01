CREATE DATABASE IF NOT EXISTS users;

USE users;

CREATE TABLE IF NOT EXISTS users(
    id_user INT PRIMARY KEY AUTO_INCREMENT,
    nom_user VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL DEFAULT 'user'
);

INSERT IGNORE INTO users (nom_user, password, role)
VALUES (
    'admin',
    '$2b$12$O8qVQ6Qdx4AiZz9URgc7xuJFWHkEuMsgsjlqpFmKdDQvF3s1YkiLy',
    'admin'
);