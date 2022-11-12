#!/usr/bin/python3
import os
import argparse
from page_loader import download


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

    print(download(args.URL, args.output))


if __name__ == '__main__':
    main()
