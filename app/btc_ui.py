import requests
import streamlit as st
import pandas as pd

from halo import Halo
from config import Config

config = Config()

st.title("BTC UI")

# Let"s get the data from the API - Phoenix
ph_data = requests.get(f"{config.api_url}/profile/phoenix", headers=config.headers).json()

st.write(ph_data)
