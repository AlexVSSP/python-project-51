import os
import os.path
import requests
import logging
from bs4 import BeautifulSoup
from page_loader.names import make_file_name_html, make_dir_name
from progress.bar import IncrementalBar
from page_loader.parse_resources import parse_resources
from page_loader.download_resouces import download_resource


py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s "
                                 "%(message)s")

py_handler.setFormatter(py_formatter)
py_logger.addHandler(py_handler)


# flake8: noqa: C901
def download(url, output=os.getcwd()):
    py_logger.info(f"Module 'download' starts working")
    py_logger.info(f"The following url is entered: {url}")
    py_logger.info(f"Entered path to save a page: {output}")

    if not os.access(output, os.W_OK):
        py_logger.error(f"There are no write permissions in the specified directory: {output}")
        raise PermissionError(f"There are no write permissions in the specified directory: {output}")

    # Making path to HTML file
    url_html = make_file_name_html(url)
    file_path = os.path.join(output, url_html)
    if os.path.isfile(file_path):
        py_logger.error(f"File with the specified name {file_path} already exists")
        raise FileExistsError(f"File with the specified name {file_path} already exists")
    py_logger.info(f"File location is on: {file_path}")

    # Making directory name and path
    dir_name = make_dir_name(url)
    dir_path = os.path.join(output, dir_name)

    # Getting HTML file
    response = requests.get(url)
    if response.status_code != 200:
        py_logger.error(f"Status code from {url} is {response.status_code}")
        raise ConnectionError(f"Status code from {url} is {response.status_code}")
    file = response.text

    # Work with page
    with open(file_path, 'w+') as fp:
        soup = BeautifulSoup(file, 'html.parser')
        tags = soup.find_all(['img', 'link', 'script'])

        # Resources search and link substitution in html file
        resources_for_download = parse_resources(url, tags)

        # Create directory
        if resources_for_download:
            os.mkdir(dir_path)
            if not os.path.isdir(dir_path):
                py_logger.error(f"Specified directory {dir_path} is missing")
                raise NotADirectoryError(f"Specified directory {dir_path} is missing")
            py_logger.info(f"Directory with resources is on: {dir_path}")

            bar = IncrementalBar("Downloading resources", max=len(resources_for_download))

            # Download resources
            for resource in resources_for_download:
                download_resource(url, dir_path, resource)
                py_logger.info(f"Resource downloaded: {resource}")
                bar.next()
            bar.finish()

        # Saving html file
        bar = IncrementalBar("Downloading page", max=1, suffix='%(percent)d%%')
        fp.write(soup.prettify())
        bar.next()
        bar.finish()

    py_logger.info(f"Result of 'download' function is on: {file_path}")
    return file_path
