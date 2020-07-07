-- In 13.sql, write a SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred.
-- Your query should output a table with a single column for the name of each person.
-- There may be multiple people named Kevin Bacon in the database. Be sure to only select the Kevin Bacon born in 1958.
-- Kevin Bacon himself should not be included in the resulting list.

SELECT DISTINCT people.name
FROM movies
LEFT JOIN stars ON movies.id = stars.movie_id
LEFT JOIN people ON stars.person_id = people.id
WHERE movies.title IN
(
    SELECT movies.title
    FROM movies
    LEFT JOIN stars ON movies.id = stars.movie_id
    LEFT JOIN people ON stars.person_id = people.id
    WHERE people.id =
    (
        SELECT people.id
        FROM people
        WHERE people.name = "Kevin Bacon" AND people.birth = "1958"
    )
)
AND people.id !=
(
    SELECT people.id
    FROM people
    WHERE people.name = "Kevin Bacon" AND people.birth = "1958"
)
;