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

    except ConnectionError:
        print(f"Unable to connect to {args.URL}")
        script_logger.error(f"Unable to connect to {args.URL}")
        sys.exit(1)

    except FileExistsError as file_exists_e:
        print(file_exists_e)
        script_logger.error(f"Error: {file_exists_e}")
        sys.exit(1)

    except FileNotFoundError as file_not_found_e:
        print(file_not_found_e)
        script_logger.error(f"Error: {file_not_found_e}")
        sys.exit(1)

    except InterruptedError as interrupted_e:
        print(interrupted_e)
        script_logger.error(f"Error: {interrupted_e}")
        sys.exit(1)

    except IsADirectoryError as is_a_directory_e:
        print(is_a_directory_e)
        script_logger.error(f"Error: {is_a_directory_e}")
        sys.exit(1)

    except NotADirectoryError as not_a_directory_e:
        print(not_a_directory_e)
        script_logger.error(f"Error: {not_a_directory_e}")
        sys.exit(1)

    except PermissionError as permission_e:
        print(permission_e)
        script_logger.error(f"Error: {permission_e}")
        sys.exit(1)

    except ProcessLookupError as process_look_up_e:
        print(process_look_up_e)
        script_logger.error(f"Error: {process_look_up_e}")
        sys.exit(1)

    except TimeoutError as timeout_e:
        print(timeout_e)
        script_logger.error(f"Error: {timeout_e}")
        sys.exit(1)

    else:
        script_logger.info(f'The command line utility "page-loader" has finished')
        sys.exit(0)


if __name__ == '__main__':
    main()
