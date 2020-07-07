-- In 10.sql, write a SQL query to list the names of all people who have directed a movie that received a rating of at least 9.0.
-- Your query should output a table with a single column for the name of each person.

SELECT DISTINCT people.name
FROM movies
LEFT JOIN directors ON movies.id = directors.movie_id
LEFT JOIN people ON directors.person_id = people.id
LEFT JOIN ratings ON movies.id = ratings.movie_id
WHERE ratings.rating >= "9.0" AND directors.person_id IS NOT NULL AND people.name IS NOT NULL AND ratings.rating IS NOT NULL;