from ss13stats.db import Server, GlobalStat, ServerStat, db_ext

from datetime import datetime

import requests

import urllib.parse

import os.path

SS14_HUB_URL = "https://central.spacestation14.io/hub/api/servers"
SS14_DEFAULT_PORT = 1212

live_games = requests.get(SS14_HUB_URL).json()

now = datetime.utcnow().replace(second=0, microsecond=0) # Get current time truncated to the minute

total_player_count = 0

for server in Server.query.all():
	server.player_count = 0 # reset all servers to zero so if they're not on the list they don't stay at whatever they were at
	server.online = 0 # assume all previously tracked servers not in the hub list are offline

for game in live_games:
	addr = game["address"]
	title = game["name"]

	parse = urllib.parse.urlparse(addr)

	if parse.scheme == "ss14s":
		scheme = "https"
	elif parse.scheme == "ss14":
		scheme = "http"

	http_addr = urllib.parse.ParseResult(
		scheme=scheme,
		netloc=parse.netloc if parse.port else f"{parse.netloc}:{SS14_DEFAULT_PORT if scheme == 'http' else 443}",
		path=parse.path,
		params=None,
		query=parse.query,
		fragment=None
	).geturl()

	online = 0

	try:
		status_url = http_addr.rstrip("/") + "/status"

		game_stats = requests.get(status_url, timeout=2).json()
		
		if game_stats:
			title = game_stats["name"]
			player_count = game_stats["players"]
			online = 1
	
	except:
		pass

	server = Server.from_address(game["address"])

	if not online:
		player_count = 0

	if not server:
		server = Server(
			address = addr,
			first_seen = now,
			last_seen = now,
			title = title,
			player_count = player_count,
			online = online
		)

		db_ext.session.add(server)
		db_ext.session.flush()

	server.last_seen = now
	server.online = online
	server.title = title
	server.player_count = player_count

	if online:
		server_stat = ServerStat(
			timestamp = now,
			server_id = server.id,
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

db_ext.session.commit()
