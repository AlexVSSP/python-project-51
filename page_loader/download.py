import os
import os.path
import requests
# import re
import logging
from bs4 import BeautifulSoup
# from urllib.parse import urlparse, urljoin
from page_loader.names import make_file_name_html, make_dir_name
# make_file_name_image_asset, make_file_name_image_https
from page_loader.download_recouces import download_image


py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
# py_handler.setLevel(logging.INFO)
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

    # # Creating a directory
    # dir_name = make_dir_name(url)
    # dir_path = os.path.join(output, dir_name)
    # os.mkdir(dir_path)
    # py_logger.info(f"Directory with resources is on: {dir_path}")

    # Getting HTML file
    response = requests.get(url)
    if response.status_code != 200:
        py_logger.error(f"Status code from {url} is {response.status_code}")
        raise ConnectionError(f"Status code from {url} is {response.status_code}")
    # print(f"Response is {response}")
    file = response.text

    # Creating a directory
    dir_name = make_dir_name(url)
    dir_path = os.path.join(output, dir_name)
    os.mkdir(dir_path)
    if not os.path.isdir(dir_path):
        py_logger.error(f"Specified directory {dir_path} is missing")
        raise NotADirectoryError(f"Specified directory {dir_path} is missing")
    py_logger.info(f"Directory with resources is on: {dir_path}")

    # Work with page
    # with open(file_path, 'w+') as fp:
    with open(file_path, 'w+') as fp:
        soup = BeautifulSoup(file, 'html.parser')
        # Find all images on page
        for link in soup.find_all('img'):
            link_path = link.get('src')
            # /assets/....jpg  !!! DON'T FORGET TO MAKE A CHECK
            # IF NETLOC IN IMAGE AND SITE ARE THE SAME !!!
            link['src'] = download_image(url, dir_name, link_path)
            py_logger.info(f"Downloaded image has name: {link['src']}")

        for link in soup.find_all('link'):
            link_path = link.get('href')
            link['href'] = download_image(url, dir_name, link_path)
            py_logger.info(f"Downloaded link has name: {link['href']}")

        for link in soup.find_all('script'):
            link_path = link.get('src')
            if link_path is not None:
                link['src'] = download_image(url, dir_name, link_path)
                py_logger.info(f"Downloaded script has name: {link['src']}")

        fp.write(soup.prettify())

    py_logger.info(f"Result of 'download' function is on: {file_path}")
    return file_path
