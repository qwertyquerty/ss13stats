from decimal import DivisionByZero
from ss13stats import rest_ext
from ss13stats.db import Server, ServerSchema, GlobalStat, GlobalStatSchema, ServerStat, ServerStatSchema

from datetime import datetime, timedelta

from flask_apispec import MethodResource, use_kwargs, marshal_with

import marshmallow
from marshmallow import Schema, fields

from sqlalchemy import func

class ServerListResource(MethodResource):
	@marshal_with(ServerSchema(many=True))
	def get(self, **kwargs):
		return Server.query.all()


class ServerStatsQuerySchema(Schema):
	server_id = fields.Integer(required=True)
	grouping = fields.String(validate=marshmallow.validate.OneOf(["HOUR", "DAY", "MONTH", "YEAR"]))
	limit = fields.Integer()

class ServerStatsResource(MethodResource):
	@marshal_with(ServerStatSchema(many=True))
	@use_kwargs(ServerStatsQuerySchema)
	def get(self, **kwargs):
		return ServerStat.get_stats(kwargs["server_id"], grouping=kwargs.get("grouping"), limit=kwargs.get("limit"))


class GlobalStatsQuerySchema(Schema):
	type = fields.String(validate=marshmallow.validate.OneOf(["SERVER_COUNT", "PLAYER_COUNT", "FAN_COUNT"]), required=True)
	grouping = fields.String(validate=marshmallow.validate.OneOf(["HOUR", "DAY", "MONTH", "YEAR"]))
	limit = fields.Integer()

class GlobalStatsResource(MethodResource):
	@marshal_with(GlobalStatSchema(many=True))
	@use_kwargs(GlobalStatsQuerySchema)
	def get(self, **kwargs):
		return GlobalStat.get_stats(kwargs["type"], grouping=kwargs.get("grouping"), limit=kwargs.get("limit"))



class CurseResource(MethodResource):
	def get(self, **kwargs):
		import requests
		from flask import jsonify
		from sklearn.linear_model import LinearRegression
		import numpy as np

		ss13 = requests.get(f"https://ss13.qtqt.cf/api/global_stats?type=PLAYER_COUNT&grouping=DAY").json()
		ss14 = requests.get(f"https://ss14.qtqt.cf/api/global_stats?type=PLAYER_COUNT&grouping=DAY").json()


		x = list(range(len(ss13)))

		r1 = LinearRegression().fit(np.array(x).reshape(-1, 1), np.asarray([x["value"] for x in ss13]).reshape(-1, 1))
		r2 = LinearRegression().fit(np.array(x[-len(ss14):]).reshape(-1, 1), np.asarray([x["value"] for x in ss14]).reshape(-1, 1))

		try:
			intersection = (r2.intercept_[0] - r1.intercept_[0]) / (r1.coef_[0][0] - r2.coef_[0][0])
			days_until_broken = int(round(intersection - len(x), 0))
			
		except DivisionByZero:
			days_until_broken = None

		return jsonify({
			"ss13": ss13,
			"ss14": ss14,
			"days_until_broken": days_until_broken
		})


class GlobalWeekdayAveragesResource(MethodResource):
	@marshal_with(GlobalStatSchema(many=True))
	def get(self, **kwargs):
		return GlobalStat.get_weekday_averages()


class ServerWeekdayAveragesResource(MethodResource):
	@marshal_with(ServerStatSchema(many=True))
	@use_kwargs(ServerStatsQuerySchema)
	def get(self, **kwargs):
		return ServerStat.get_weekday_averages(kwargs["server_id"])


class GlobalHourlyAveragesResource(MethodResource):
	@marshal_with(GlobalStatSchema(many=True))
	def get(self, **kwargs):
		return GlobalStat.get_hourly_averages()


class ServerHourlyAveragesResource(MethodResource):
	@marshal_with(ServerStatSchema(many=True))
	@use_kwargs(ServerStatsQuerySchema)
	def get(self, **kwargs):
		return ServerStat.get_hourly_averages(kwargs["server_id"])



class SummarySchema(Schema):
	data_point_count = fields.Integer()
	server_count = fields.Integer()
	active_server_count = fields.Integer()
	player_count = fields.Integer()
	last_updated = fields.DateTime()

class SummaryResource(MethodResource):
	@marshal_with(SummarySchema)
	def get(self, **kwargs):
		most_recently_updated_server = Server.query.order_by(Server.last_seen.desc()).first()

		return {
			"data_point_count": GlobalStat.query.count() + ServerStat.query.count(),
			"server_count": Server.query.count(),
			"active_server_count": Server.query.filter(Server.online == 1).count(),
			"player_count": Server.query.with_entities(func.sum(Server.player_count)).scalar(),
			"last_updated": most_recently_updated_server.last_seen if most_recently_updated_server else None
		}
