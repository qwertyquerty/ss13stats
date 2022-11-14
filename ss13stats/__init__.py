from ss13stats.config import cfg
from ss13stats.util import *

from flask import Flask, render_template, send_from_directory

from flask_marshmallow import Marshmallow

from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy

from webargs.flaskparser import parser

flask = Flask(__name__)

flask.config.update({
    "SQLALCHEMY_DATABASE_URI": f"mysql+mysqlconnector://{cfg.get('db.user')}:{cfg.get('db.pass')}@{cfg.get('db.host')}:{cfg.get('db.port')}/{cfg.get('db.name')}?charset=utf8mb4",
})

db_ext = SQLAlchemy(flask)

ma_ext = Marshmallow(flask)

rest_ext = Api(flask)

parser.location = "query"

from ss13stats.resources import *

@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    abort_with_msg(err.messages, 400)

@flask.route("/static/<path:path>")
def send_static_content(path):
    return send_from_directory("static", path)

@flask.route("/")
def home_page():
	return render_template("index.html")

@flask.route("/hub")
def hub_page():
	servers = Server.get_hub_list()

	return render_template("hub.html", servers=servers)

@flask.route("/curse")
def curse_page():
	return render_template("curse.html")

@flask.route("/hub/<int:server_id>")
def server_page(server_id):
	server = Server.query.get_or_404(server_id)

	return render_template("server.html", server=server)

@flask.after_request
def after_request(response):
    response.access_control_allow_origin = "*"
    return response


rest_ext.add_resource(ServerListResource, "/api/servers")
rest_ext.add_resource(ServerStatsResource, "/api/server_stats")
rest_ext.add_resource(GlobalStatsResource, "/api/global_stats")
rest_ext.add_resource(CurseResource, "/api/curse")
rest_ext.add_resource(SummaryResource, "/api/summary")
rest_ext.add_resource(GlobalWeekdayAveragesResource, "/api/global_weekdays")
rest_ext.add_resource(ServerWeekdayAveragesResource, "/api/server_weekdays")
rest_ext.add_resource(GlobalHourlyAveragesResource, "/api/global_hours")
rest_ext.add_resource(ServerHourlyAveragesResource, "/api/server_hours")
