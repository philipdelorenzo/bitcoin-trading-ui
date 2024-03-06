import os
import time
import dotenv
import configparser
from dataclasses import dataclass

BASE = os.path.abspath(os.path.dirname(__file__))
MAIN = os.path.abspath(os.path.join(BASE, ".."))

_config = configparser.ConfigParser()
_config.read(os.path.join(BASE, "config.ini"))
dotenv.load_dotenv(os.path.join(MAIN, ".env"))

@dataclass
class Config():
    """Class for maintaining the configuration"""
    _host = _config["api"]["host"]
    _port = _config["api"]["port"]

    btc_app_robinhood_api_key = os.getenv("BTC_APP_ROBINHOOD_API_KEY")

    ### Let"s set configuration
    headers = {
        "accept": "application/json",
        "x-api-key": btc_app_robinhood_api_key,
        }
    
    # API URL
    api_url = f"http://{_host}:{_port}"
