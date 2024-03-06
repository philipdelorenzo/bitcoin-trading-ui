import json
import requests
import streamlit as st
import pandas as pd

from config import Config
from st_pages import Page, show_pages, add_page_title

config = Config()
st.set_page_config(layout="wide")

headlines = requests.get(f"{config.api_url}/headlines", headers=config.headers).json()