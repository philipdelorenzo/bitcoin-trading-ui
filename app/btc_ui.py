import json
import requests
import streamlit as st
import pandas as pd

from config import Config
from st_pages import Page, show_pages, add_page_title

config = Config()
st.set_page_config(layout="wide")

# This is the sidebar configuration
show_pages(
    [
        Page("app/btc_ui.py", "Home"),
        Page("app/pages/headlines.py", "Headlines"),
        Page("app/pages/transactions.py", "Transactions"),
    ]
)

# Let"s get the data from the API - Phoenix
with st.spinner("Retrieving data from Robinhood..."):
    current_invested_symbols = requests.get(f"{config.api_url}/crypto/current_coins", headers=config.headers).json()
    ph_data = requests.get(f"{config.api_url}/profile/phoenix", headers=config.headers).json()
    quote_data = requests.get(f"{config.api_url}/crypto/quotes", headers=config.headers).json()

# Let's display the order history
tables1, tables2 = st.columns([1,1])
order_history = requests.get(f"{config.api_url}/crypto/order_history", headers=config.headers).json()

with tables1:
    st.title("Percentage Change")
    c1, c2, c3 = st.columns([1,1,1])
    for coin in current_invested_symbols:
        coin_transact = [i for i in order_history if i["currency_code"] == coin]
        last_transaction = coin_transact[-1]
        last_transaction_date = last_transaction["last_transaction_at"].split("T")[0]
        current_price = quote_data[coin]["mark_price"]
        purchased_price = last_transaction["price"]
        quantity = str(last_transaction["quantity"])

        _pp = '${:,.2f}'.format(float(purchased_price))
        _cp = '${:,.2f}'.format(float(current_price))
        percentage_change = '%{:,.2f}'.format((float(current_price) - float(purchased_price)) / float(purchased_price) * 100)
        
        with c1:
            st.metric(label=f"{coin}: Purchase Price", value=_pp)
        with c2:
            st.metric(label=f"{coin}: Percentage Change", value=_cp, delta=percentage_change)

        with c3:
            # Let's display how much money we would make if we sold the stock
            st.metric(label=f"{coin}: Current Price", value=_cp, delta='${:,.2f}'.format(float(current_price) * float(quantity)))
            st.caption(f"If you sold all your {coin} coins at the current price, this is your profit.")

with tables2:
    st.title("Order History - Last 25")
    df = pd.DataFrame(columns=[
        "Currency",
        "Date",
        "Time",
        "Effective Price",
        "Purchage Type",
        "Coin Quantity",
        "Average Price",
        "Transaction Type"
    ])

    for i in range(25):
        df.loc[i] = [
            order_history[i]["currency_code"],
            order_history[i]["last_transaction_at"].split("T")[0],
            order_history[i]["last_transaction_at"].split("T")[1].split(".")[0],
            '${:,.2f}'.format(float(order_history[i]["price"])),
            order_history[i]["type"],
            order_history[i]["quantity"],
            '${:,.2f}'.format(float(order_history[i]["average_price"])),
            order_history[i]["side"],
            ]

    st.dataframe(df)

# Let's add a separator
st.markdown("""<hr style="height:px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

st.title("Profile Data and Health")
col1, col2, col3, col4 = st.columns([1,1,1,1], gap="small")

with col1:
    st.metric(label="Crypto Investments", value=ph_data["crypto"]["equity"]["amount"])

with col2:
    st.metric(label="Buying Power", value=ph_data["crypto_buying_power"]["amount"])

with col3:
    st.metric(label="Withdrawlable Cash", value=ph_data["withdrawable_cash"]["amount"])

with col4:
    st.metric(label="Margin Health", value=ph_data["margin_health"]["margin_health_state"])

# Let's add a separator
st.markdown("""<hr style="height:px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

# Let's display the current coins
sec1, sec2, sec3 = st.columns([1,1,1])

with sec1:
    st.title("Owned Coins")
    for coin in current_invested_symbols:
        st.metric(label=coin, value=
                current_invested_symbols[coin])

with sec2:
    st.title("Coin Values - USD")
    for coin in current_invested_symbols:
        st.metric(label=coin, value='${:,.2f}'.format(float(quote_data[coin]["mark_price"])))
          
with sec3:
    st.title("Coin Investment - USD")
    for coin in current_invested_symbols:
        st.metric(label=coin, value='${:,.2f}'.format(float(quote_data[coin]["mark_price"]) * float(current_invested_symbols[coin])))

######## Let's calculate the owned coins in USD ########
for coin in current_invested_symbols:
    coin_transact = [i for i in order_history if i["currency_code"] == coin]
    last_transaction = coin_transact[-1]
    cash = ph_data["crypto_buying_power"]["amount"]
    purchased_price = last_transaction["price"]
    current_price = quote_data[coin]["mark_price"]
    percentage_change = '{:,.2f}'.format((float(current_price) - float(purchased_price)) / float(purchased_price) * 100)

    print(f"Sending calcluation request for coin: {coin}, purchased_price: {'${:,.2f}'.format(float(purchased_price))}, current_price: {'${:,.2f}'.format(float(current_price))}, percentage_change: {percentage_change}")
    _params = {
        "symbol": coin,
        "cash": cash,
        "number_of_investments": len(current_invested_symbols),
        "purchased_price": purchased_price,
        "current_price": current_price,
        "percentage_change": percentage_change
        }
    
    results = requests.post(f"{config.api_url}/markets/calculate", headers=config.headers, params=_params).json()
