from ss13stats.db import Server, GlobalStat, ServerStat, db_ext

from bs4 import BeautifulSoup

from datetime import datetime

import re

import requests

BYOND_GAME_URL = "http://www.byond.com/games/Exadv1/SpaceStation13"

# Sorry for whoever has to deal with this regex in the future
PLAYER_COUNT_REGEX = re.compile(r" ([0-9]{1,3}|No) players?(?:\.|(?s:.*)\[See list\])")

document = requests.get(BYOND_GAME_URL).text

soup = BeautifulSoup(document, 'html.parser')

now = datetime.utcnow().replace(second=0, microsecond=0) # Get current time truncated to the minute

fan_count = int(soup.find(id="hub_overview").tr.td.div.div.span.a.text.split(" ")[0])

live_games = soup.find_all("div", class_="live_game_entry")

total_player_count = 0

for game in live_games:
	server_url = game.div.div.span.nobr.text

	server_id = int(server_url.split(".")[-1])

	player_count_parse = PLAYER_COUNT_REGEX.search(game.div.div.text).groups(0)[0]

	if game.div.div.find("b"):
		title = game.div.div.find("b").text
	else:
		title = server_url

	player_count = int(player_count_parse) if player_count_parse != "No" else 0

	server = Server.query.get(server_id)

	if not server:
		server = Server(
			id = server_id,
			first_seen = now,
			last_seen = now,
			title = title,
			player_count = player_count
		)

		db_ext.session.add(server)

	server.last_seen = now
	server.title = title
	server.player_count = player_count

	server_stat = ServerStat(
		timestamp = now,
		server_id = server_id,
		player_count = player_count
	)

	db_ext.session.add(server_stat)

	total_player_count += player_count

db_ext.session.add(GlobalStat(
	timestamp = now,
	type = "SERVER_COUNT",
	value = len(live_games)
))

db_ext.session.add(GlobalStat(
	timestamp = now,
	type = "PLAYER_COUNT",
	value = total_player_count
))

db_ext.session.add(GlobalStat(
	timestamp = now,
	type = "FAN_COUNT",
	value = fan_count
))

db_ext.session.commit()
