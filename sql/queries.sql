USE wellbe_rpa;

SELECT * FROM movies;

SELECT COUNT(*) AS total_movies
FROM movies;

SELECT movie_name, created_at
FROM movies
ORDER BY id ASC;