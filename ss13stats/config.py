from dotenv import load_dotenv
from envyaml import EnvYAML

load_dotenv("./config.env")

cfg = EnvYAML("./config.yml")
