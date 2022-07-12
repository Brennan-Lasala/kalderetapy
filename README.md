# kalderetapy
A small app that can monitor the `executionReport` websocket message delay for X ms.
It has a client application that can send a basic order.
It also has a websocket client application listen to user data stream.


## Requirements and Installation
-----
- Python 3.8.3
- Python dependencies located under `requirements.txt`
- Install with `pip -r requirements.txt`

## Basic Order Client application
-----
### Required fields as follows:
- Symbol(-S, --symbol) (BNBBTC, BNBBUSD, BNBUSDT, BTCBUSD, BTCUSDT, ETHBTC, ETHBUSD, ETHUSDT, LTCBNB, LTCBTC, LTCBUSD, LTCUSDT, TRXBNB, TRXBTC, TRXBUSD, TRXUSDT, XRPBNB, XRPBTC, XRPBUSD, XRPUSDT)
- Side(-s, --side) BUY/SELL
- Type(-t, --type) (LIMIT, MARKET, STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER) see https://www.binance.com/en/support/faq/360033779452 for more information
- TimeInForce(-T, --time-in-force) (GTC, IOC, FOK)
- Quantity(-q, --quantity) quantity of symbol
- Price(-p, --price) price of symbol
### Optional fields as follows:
- ReceivingWindow(-r, --recv-window) Receiving window, default(5000ms)
- Base Url(-b, --base-url) defaults to `https://testnet.binance.vision`
- Config Path(-c, --config) path to config file containing API keys and Secret Key

```shell
Send a sample buy order:
python3 order_main.py \
    --side BUY \
    --symbol LTCBTC \
    --type LIMIT \
    --time-in-force GTC \
    --quantity 1 \
    --price 0.002 \
    --recv-window 5000
```

## Listen Client application
-----
### Required fields as follows:
- Delay(-d, --delay) Delay threshold(ms) to send an alert, based on client local time difference
### Optional fields as follows:
- Base Url(-b, --base-url) defaults to `https://testnet.binance.vision`
- Config Path(-c, --config) path to config file containing API keys and Secret Key
```shell
Start listen_client application:
python3 listen_client.py \
    --delay 500
```

### Configuring Secrets
1. Get API key and Secret key from https://testnet.binance.vision/ after logging in with Github.
1. Generate an API Key https://testnet.binance.vision/key/generate.
1. Copy paste you key and save locally.
1. Open `secrets.cfg` and replace the appropriate `<INSERT KEY HERE>` key value pair.
1. Save `secrets.cfg` file.
