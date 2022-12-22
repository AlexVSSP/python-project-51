#!/usr/bin/python3
import os
import argparse
import logging
import sys
from page_loader import download


script_logger = logging.getLogger(__name__)
script_logger.setLevel(logging.INFO)

py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s "
                                 "%(message)s")

py_handler.setFormatter(py_formatter)
script_logger.addHandler(py_handler)


# flake8: noqa: C901
def main():
    parser = argparse.ArgumentParser(prog='page-loader',
                                     description='Download page from web '
                                                 'and shows a path '
                                                 'to directory '
                                                 'of this page.')
    parser.add_argument('URL')
    parser.add_argument('-o', '--output',
                        help='set path to save a page', default=os.getcwd())
    args = parser.parse_args()

    script_logger.info(f'The command line utility "page-loader" is running')

    try:
        print(download(args.URL, args.output))

    except Exception as exc:
        print(exc)
        script_logger.error(f"Error: {exc}")
        sys.exit(1)

    else:
        script_logger.info(f'The command line utility "page-loader" has finished')
        sys.exit(0)


if __name__ == '__main__':
    main()
