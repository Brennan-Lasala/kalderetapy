import argparse
import configparser
import os.path
import sys
from typing import Tuple

import basic_order_client as boc
import binance_api


def __key_extraction(config_file) -> Tuple[str, str]:
    config = configparser.ConfigParser()
    config.read(config_file)
    if 'SECRETS' not in config:
        print(f'The {config_file} file has been tampered, please revert to '
              'stable version', file=sys.stderr)
        sys.exit(1)
    if (config['SECRETS']['api_key'] == '<INSERT KEY HERE>' or
            config['SECRETS']['secret_key'] == '<INSERT KEY HERE>'):
        print('Please provide/setup valid API and Secret key to '
              f'{config_file}', file=sys.stderr)
        sys.exit(1)
    return config['SECRETS']['api_key'], config['SECRETS']['secret_key']


def config_validation(config_file):
    if os.path.exists(config_file):
        return __key_extraction(config_file)
    else:
        print(f'{config_file} file does not exist, please provide a '
              'valid cfg file or use default(secrets.cfg)', file=sys.stderr)
        sys.exit(1)


def main():
    api_key = ''
    secret_key = ''
    parser = argparse.ArgumentParser(
        description='Basic order placement client.')
    parser.add_argument('-b', '--base-url', dest='base_url',
                        default=binance_api.BASE_URL,
                        help=('base url for your API calls, '
                              f'default({binance_api.BASE_URL})'))
    parser.add_argument('-c', '--config', dest='config', default='secrets.cfg',
                        help='config file for secrets, containing API key and '
                             'Secret key')
    parser.add_argument('-p', '--price', dest='price', required=True,
                        help='target price')
    parser.add_argument('-q', '--quantity', dest='quantity', required=True,
                        help='target quantity')
    parser.add_argument('-s', '--side', dest='side', required=True,
                        help='(BUY/SELL) side')
    parser.add_argument('-S', '--symbol', dest='symbol', required=True,
                        help='Target symbol or ticker')
    parser.add_argument('-t', '--type', dest='type', required=True,
                        help='(LIMIT, MARKET, STOP_LOSS, STOP_LOSS_LIMIT, '
                        'TAKE_PROFIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER) see '
                        'https://www.binance.com/en/support/faq/360033779452 '
                        'for more information')
    parser.add_argument('-T', '--time-in-force', dest='time_in_force',
                        required=True, help='(GTC, IOC, FOK)')
    parser.add_argument('-r', '--recv-window', dest='recv_window',
                        default=5000, help='Receiving window default(5000ms)')
    args = parser.parse_args()
    api_key, secret_key = config_validation(args.config)
    app = boc.BasicOrderClient(args.base_url, api_key,
                               secret_key, args)
    app.run()


if __name__ == "__main__":
    main()
