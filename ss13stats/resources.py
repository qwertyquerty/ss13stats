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


class SummarySchema(Schema):
	data_point_count = fields.Integer()
	server_count = fields.Integer()
	player_count = fields.Integer()

class SummaryResource(MethodResource):
	@marshal_with(SummarySchema)
	def get(self, **kwargs):
		return {
			"data_point_count": GlobalStat.query.count() + ServerStat.query.count(),
			"server_count": Server.query.count(),
			"player_count": Server.query.with_entities(func.sum(Server.player_count)).scalar()
		}
