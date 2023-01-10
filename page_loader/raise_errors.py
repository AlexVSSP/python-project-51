import os
import logging


py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s "
                                 "%(message)s")

py_handler.setFormatter(py_formatter)
py_logger.addHandler(py_handler)


# flake8: noqa: C901
def raise_file_system_error(output, file_path):
    if not os.access(output, os.W_OK):
        py_logger.error(f"There are no write permissions in the specified directory: {output}")
        raise PermissionError(f"There are no write permissions in the specified directory: {output}")
    elif os.path.isfile(file_path):
        py_logger.error(f"File with the specified name {file_path} already exists")
        raise FileExistsError(f"File with the specified name {file_path} already exists")


def raise_connection_error(url, response):
    if response.status_code != 200:
        py_logger.error(f"Status code from {url} is {response.status_code}")
        raise ConnectionError(f"Status code from {url} is {response.status_code}")


def raise_not_a_directory_error(dir_path):
    if not os.path.isdir(dir_path):
        py_logger.error(f"Specified directory {dir_path} is missing")
        raise NotADirectoryError(f"Specified directory {dir_path} is missing")
