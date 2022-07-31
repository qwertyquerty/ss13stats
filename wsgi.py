from ss13stats import flask
from ss13stats.config import cfg

if __name__ == "__main__":
	flask.run(debug=True, port=cfg.get("website.port"))
