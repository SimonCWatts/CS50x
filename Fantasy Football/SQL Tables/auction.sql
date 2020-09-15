SELECT *
FROM bidlist
LEFT JOIN players ON bidlist.playerid = players.playerid
LEFT JOIN users ON bidlist.userid = users.id
;