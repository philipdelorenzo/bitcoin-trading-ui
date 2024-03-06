import os
import dotenv
import requests
import configparser

BASE = os.path.abspath(os.path.dirname(__file__))
MAIN = os.path.abspath(os.path.join(BASE, ".."))

_config = configparser.ConfigParser()
_config.read(BASE, "config.ini")
dotenv.load_dotenv(os.path.join(MAIN, ".env"))
_host = _config["api"]["host"]
_port = _config["api"]["port"]
_api_url = f"http://{_host}:{_port}"

# Let"s ensure that the .env file is present
if not os.path.exists(os.path.join(MAIN, ".env")):
    raise FileNotFoundError("The .env file is missing")

# Let"s check if the API is running
_data = requests.get(f"{_api_url}/health").json()
if not _data["status"] == 200:
    raise ConnectionError("The API is not running")

del _data
