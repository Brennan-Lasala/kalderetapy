import argparse
import json
import time
import websocket

import basic_order_client as boc
import binance_api
import order_main

target_delay = None


def on_open(ws):
    print('Connected')


def on_message(ws, message: str):
    global target_delay
    epoch_time = int(time.time() * 1000)
    msg_dict = json.loads(message)
    if msg_dict['e'] == 'executionReport':
        execution_time = int(msg_dict['E'])
        delay_time = epoch_time - execution_time
        if delay_time > target_delay:
            print(f'Alert: Event time is delayed by {delay_time}ms, '
                  f'above the {target_delay}ms threshold')
    print(message)


def on_error(ws, error: str):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print('Connection closed')


def stream_user_data(listen_key: str):
    websocket.enableTrace(False)
    socket = f'{binance_api.WS_URL}/{listen_key}'
    ws = websocket.WebSocketApp(socket,
                                on_close=on_close,
                                on_error=on_error,
                                on_message=on_message,
                                on_open=on_open)
    ws.run_forever()


def main():
    global target_delay
    parser = argparse.ArgumentParser(
        description='Basic websocket listening application.')
    parser.add_argument('-b', '--base-url', dest='base_url',
                        default=binance_api.BASE_URL,
                        help=('base url for your API calls, '
                              f'default({binance_api.BASE_URL})'))
    parser.add_argument('-c', '--config', dest='config', default='secrets.cfg',
                        help='config file for secrets, containing API key and '
                             'Secret key')
    parser.add_argument('-d', '--delay', dest='delay', required=True, type=int,
                        help='Delay threshold(ms) to send an alert, '
                             'based on client local time difference')
    args = parser.parse_args()
    target_delay = args.delay
    api_key, secret_key = order_main.config_validation(args.config)
    app = boc.BasicOrderClient(binance_api.BASE_URL, api_key, secret_key)
    listen_key = app.create_listen_key()['listenKey']
    stream_user_data(listen_key)
    app.delete_listen_key(listen_key)


if __name__ == "__main__":
    main()
