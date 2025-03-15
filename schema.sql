CREATE DATABASE asl_detection;

USE asl_detection;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES ('testuser', 'testpassword');

select * from users;
TRUNCATE TABLE users;