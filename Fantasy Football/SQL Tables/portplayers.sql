SELECT *
FROM portfolio
LEFT JOIN players ON portfolio.playerid = players.playerid
LEFT JOIN users on portfolio.userid = users.id
WHERE users.id = session["user_id"]
;