import json
import requests
import streamlit as st
import pandas as pd

from config import Config

config = Config()

st.title("BTC UI")
current_invested_symbols = requests.get(f"{config.api_url}/crypto/current_coins", headers=config.headers).json()
col1, col2, col3, col4 = st.columns([1,1,1,1], gap="small")

# Let"s get the data from the API - Phoenix
with st.spinner("Retrieving data from Robinhood..."): 
    ph_data = requests.get(f"{config.api_url}/profile/phoenix", headers=config.headers).json()

with col1:
    st.metric(label="Crypto Investments", value=ph_data["crypto"]["equity"]["amount"])
    # Let's calculate the owned coins in USD

with col2:
    st.metric(label="Buying Power", value=ph_data["crypto_buying_power"]["amount"])

with col3:
    st.metric(label="Withdrawlable Cash", value=ph_data["withdrawable_cash"]["amount"])

with col4:
    st.metric(label="Margin Health", value=ph_data["margin_health"]["margin_health_state"])

# Let's display the current coins
sec1, sec2 = st.columns([1,1])
with sec1:
    st.title("Current Coins")
    for coin in current_invested_symbols:
        st.metric(label=coin, value=
                current_invested_symbols[coin])

with sec2:
    st.title("Current Coins USD Value")
    quote_data = requests.get(f"{config.api_url}/crypto/quotes", headers=config.headers).json()
    for coin in current_invested_symbols:
        st.metric(label=coin, value='${:,.2f}'.format(float(quote_data[coin]["mark_price"]) * float(current_invested_symbols[coin])))

# Let's display the order history
order_history = requests.get(f"{config.api_url}/crypto/order_history", headers=config.headers).json()
st.title("Order History - Last 5")

df = pd.DataFrame(columns=[
    "Currency",
    "Time Stamp",
    "Average Price",
    "Coin Quantity",
    "Effective Price",
    "Purchage Type",
    "Transaction Type"
    ])

for i in range(5):
    #st.json(order_history[i])
    df.loc[i] = [
        order_history[i]["currency_code"],
        order_history[i]["last_transaction_at"],
        order_history[i]["average_price"],
        order_history[i]["quantity"],
        order_history[i]["price"],
        order_history[i]["side"],
        order_history[i]["type"]
        ]

st.dataframe(df)
