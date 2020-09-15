SELECT users.username, SUM(players.POINTS), users.cash
FROM portfolio
LEFT JOIN users ON portfolio.userid = users.id
LEFT JOIN players on portfolio.playerid = players.PLAYERID
GROUP BY users.username;