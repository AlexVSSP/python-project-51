import os
import os.path
import requests
import logging
from page_loader.parse_resources import parse_resources
from page_loader.download_resources import download_resources
from page_loader.save_html_page import save_html_page
from page_loader.making_paths import make_file_path, make_dir_path
from page_loader.raise_errors import connection_error, not_a_directory_error, \
    file_system_error


py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s "
                                 "%(message)s")

py_handler.setFormatter(py_formatter)
py_logger.addHandler(py_handler)


def get_html(url):
    response = requests.get(url)
    connection_error(url, response)
    return response.text


def download(url, output=os.getcwd()):
    py_logger.info("Module 'download' starts working")
    py_logger.info(f"The following url is entered: {url}")
    py_logger.info(f"Entered path to save a page: {output}")

    # Making path to HTML file
    file_path = make_file_path(url, output)

    file_system_error(output, file_path)
    py_logger.info(f"File location is on: {file_path}")

    # Making directory name and path
    dir_path = make_dir_path(url, output)

    # Getting HTML file
    # def get_html():
    #     response = requests.get(url)
    #     connection_error(url, response)
    #     return response.text

    file = get_html(url)

    # Resources search and link substitution in html file
    resources_for_download, text_result = parse_resources(url, file, dir_path)

    # Create directory
    if resources_for_download:
        os.mkdir(dir_path)

        not_a_directory_error(dir_path)
        py_logger.info(f"Directory with resources is on: {dir_path}")

        # Download resources
        download_resources(url, resources_for_download)

    # Saving html file
    save_html_page(file_path, text_result)

    py_logger.info(f"Result of 'download' function is on: {file_path}")
    return file_path
