import os
import os.path
import requests
import logging
from bs4 import BeautifulSoup
from page_loader.names import make_file_name_html, make_dir_name
from page_loader.download_recouces import download_image
from progress.bar import IncrementalBar


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

    # Getting HTML file
    response = requests.get(url)
    if response.status_code != 200:
        py_logger.error(f"Status code from {url} is {response.status_code}")
        raise ConnectionError(f"Status code from {url} is {response.status_code}")
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
    with open(file_path, 'w+') as fp:
        soup = BeautifulSoup(file, 'html.parser')

        # Find all images on page
        images_count = 0
        for link in soup.find_all('img'):
            images_count += 1

        bar = IncrementalBar("Downloading images", max=images_count)
        for link in soup.find_all('img'):
            link_path = link.get('src')
            # print(f"link_path = {link_path}")
            if link_path is not None:
                link['src'] = download_image(url, dir_path, link_path)
                bar.next()
                py_logger.info(f"Downloaded image has name: {link['src']}")
        bar.finish()

        # Find all links on page
        links_count = 0
        for link in soup.find_all('link'):
            links_count += 1

        bar = IncrementalBar("Downloading links", max=links_count)
        for link in soup.find_all('link'):
            link_path = link.get('href')
            if link_path is not None:
                link['href'] = download_image(url, dir_path, link_path)
                bar.next()
                py_logger.info(f"Downloaded link has name: {link['href']}")
        bar.finish()

        # Find all scripts on page
        scripts_count = 0
        for link in soup.find_all('script', src=True):
            scripts_count += 1

        bar = IncrementalBar("Downloading scripts", max=scripts_count)
        for link in soup.find_all('script'):
            link_path = link.get('src')
            if link_path is not None:
                link['src'] = download_image(url, dir_path, link_path)
                bar.next()
                py_logger.info(f"Downloaded script has name: {link['src']}")
        bar.finish()

        bar = IncrementalBar("Downloading page", max=1, suffix='%(percent)d%%')
        fp.write(soup.prettify())
        bar.next()
        bar.finish()

    py_logger.info(f"Result of 'download' function is on: {file_path}")
    return file_path
