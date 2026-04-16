CREATE DATABASE wellbe_rpa;
USE wellbe_rpa;

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    search_term VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);