import argparse
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

assert sys.version_info[0] == 3 and sys.version_info[1] >= 6, 'Requires Python 3.6 or newer'

os.sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))


def main():
    parser = argparse.ArgumentParser(description='')
    cmd_list = (
        'api',
        'discoverer',
    )

    parser.add_argument('cmd', choices=cmd_list, nargs='?', default='')

    args = parser.parse_args()
    cmd = args.cmd

    if cmd == 'api':
        from stx_node_map.api.app import main
        main()

    if cmd == 'discoverer':
        from stx_node_map.discoverer import worker
        worker()


if __name__ == '__main__':
    main()
