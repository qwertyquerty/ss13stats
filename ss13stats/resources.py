from ss13stats import rest_ext
from ss13stats.db import Server, ServerSchema, GlobalStat, GlobalStatSchema, ServerStat, ServerStatSchema

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

class ServerStatsResource(MethodResource):
	@marshal_with(ServerStatSchema(many=True))
	@use_kwargs(ServerStatsQuerySchema)
	def get(self, **kwargs):
		return ServerStat.query.filter(ServerStat.server_id == kwargs["server_id"]).order_by(ServerStat.timestamp.asc()).all()


class GlobalStatsQuerySchema(Schema):
	type = fields.String(validate=marshmallow.validate.OneOf(["SERVER_COUNT", "PLAYER_COUNT", "FAN_COUNT"]), required=True)
	grouping = fields.String(validate=marshmallow.validate.OneOf(["HOUR", "DAY", "MONTH", "YEAR"]))

class GlobalStatsResource(MethodResource):
	@marshal_with(GlobalStatSchema(many=True))
	@use_kwargs(GlobalStatsQuerySchema)
	def get(self, **kwargs):
		return GlobalStat.get_stats(kwargs["type"], grouping=kwargs.get("grouping"))


class SummarySchema(Schema):
	data_points_count = fields.Integer()
	servers_count = fields.Integer()

class SummaryResource(MethodResource):
	@marshal_with(SummarySchema)
	def get(self, **kwargs):
		return {
			"data_point_count": GlobalStat.query.count() + ServerStat.query.count(),
			"server_count": Server.query.count(),
			"player_count": Server.query(func.sum(Server.player_count)).scalar()
		}
