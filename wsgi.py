#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""A CLI entry point for launching Quote Generator services
"""
import sys
import argparse

from qod_app.config_app import create_app


def quote_generator_cli() -> None:
    """
    Arguments:
         mode: (prod, dev or test) [required]
         --erase_recreate_db [optional]

    eg. python wsgi.py
    eg. python wsgi.py prod
    eg. python wsgi.py test --erase_recreate_db
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--dev_mode',
                        action='store_true',
                        help="launch dev mode")
    parser.add_argument('--test_mode',
                        action='store_true',
                        help="launch test mode")
    parser.add_argument('--prod_mode',
                        action='store_true',
                        help="launch production mode")
    parser.add_argument('--erase_recreate_db',
                        action='store_true',
                        help="recreate a new database [BE CAREFUL IN PRODUCTION] "
                             "| always true for dev and test mode")

    args = parser.parse_args()

    port = 3000

    if args.dev_mode:
        app = create_app(mode="dev", erase_db=args.erase_recreate_db)
    elif args.test_mode:
        app = create_app(mode="test", erase_db=args.erase_recreate_db)
    elif args.prod_mode:
        app = create_app(mode="prod", erase_db=args.erase_recreate_db)
    else:
        print("no mode specify to launch app")
        sys.exit()

    app.run(port=port)


if __name__ == '__main__':
    quote_generator_cli()
