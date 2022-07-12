import hashlib
import hmac
import requests
import sys

import binance_api


class BasicOrderClient:
    def __init__(self, base_url: str, api_key: str, secret_key: str,
                 order_args=None):
        self.base_url = base_url
        self.api_key = api_key
        self.secret_key = secret_key
        self.__all_symbols = None
        self.order_args = {}
        if order_args is not None:
            self.order_args = self.__set_order_args(order_args)

    def __get_key_params(self):
        return {'X-MBX-APIKEY': self.api_key}

    def __hashing(self) -> str:
        query_string = self.__stringify_order_args()
        return hmac.new(self.secret_key.encode('utf-8'),
                        query_string.encode('utf-8'),
                        hashlib.sha256).hexdigest()

    def __place_order(self):
        self.order_args['timestamp'] = self.get_timestamp()
        self.order_args['signature'] = self.__hashing()
        print(f'ts:{self.order_args["timestamp"]}')
        try:
            response = requests.post(self.base_url + binance_api.ORDER_URL,
                                     params=self.order_args,
                                     headers=self.__get_key_params())
        except requests.exceptions.ConnectionError as err:
            print(err, file=sys.stderr)
            sys.exit(1)
        self.verify_response(response.json())

    def __set_order_args(self, order_args) -> dict:
        args_dict = {}
        args_dict['symbol'] = order_args.symbol
        args_dict['side'] = order_args.side
        args_dict['type'] = order_args.type
        args_dict['timeInForce'] = order_args.time_in_force
        args_dict['quantity'] = order_args.quantity
        args_dict['price'] = order_args.price
        args_dict['recvWindow'] = order_args.recv_window
        return args_dict

    def __stringify_order_args(self) -> str:
        query_string = ''
        for key in self.order_args.keys():
            query_string = f'{query_string}&{key}={self.order_args.get(key)}'
        # removes the 1st & in the string
        return query_string[1:]

    @property
    def all_symbols(self):
        if self.__all_symbols is None:
            response = requests.get(self.base_url + binance_api.EXCHANGE_URL)
            symbol_dict = response.json()['symbols']
            self.__all_symbols = [symbol['symbol'] for symbol in symbol_dict]
        return self.__all_symbols

    def create_listen_key(self):
        try:
            response = requests.post(self.base_url + binance_api.LISTEN_URL,
                                     headers=self.__get_key_params())
        except requests.exceptions.ConnectionError as err:
            print(err, file=sys.stderr)
            sys.exit(1)
        return response.json()

    def delete_listen_key(self, listen_key: str):
        params = {'listenKey': listen_key}
        try:
            response = requests.delete(self.base_url + binance_api.LISTEN_URL,
                                       params=params,
                                       headers=self.__get_key_params())
            self.verify_response(response.json())
        except requests.exceptions.ConnectionError as err:
            print(err, file=sys.stderr)
            sys.exit(1)

    def get_timestamp(self):
        try:
            response = requests.get(self.base_url
                                    + binance_api.SERVER_TIME_URL)
        except requests.exceptions.ConnectionError as err:
            print(err, file=sys.stderr)
            sys.exit(1)
        return response.json()['serverTime']

    def verify_response(self, rsp: dict):
        if 'code' in rsp:
            print(f"Error code: {rsp['code']}")
            print(f"Message: {rsp['msg']}")
            print('Please visit '
                  'https://binance-docs.github.io/apidocs/spot/en '
                  'API documentation for more information')
        else:
            print(rsp)

    def verify_symbol(self, symbol: str) -> bool:
        return symbol in self.all_symbols

    def run(self):
        self.__place_order()
