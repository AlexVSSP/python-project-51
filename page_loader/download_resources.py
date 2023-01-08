import requests
import logging
from urllib.parse import urlparse, urljoin
from progress.bar import IncrementalBar


py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s "
                                 "%(message)s")

py_handler.setFormatter(py_formatter)
py_logger.addHandler(py_handler)


def get_image(link):
    image = requests.get(link)
    return image.content


def download_resource(resource_path, link):
    with open(resource_path, 'wb') as f:
        f.write(get_image(link))


def download_resources(url, resources):
    link_path_parse = urlparse(url)
    bar = IncrementalBar("Downloading resources", max=len(resources))
    for resource in resources:

        link_path, resource_path = resource
        asset_link = urljoin(url, link_path)

        # def get_image(link):
        #     image = requests.get(link)
        #     return image.content

        if link_path.startswith(f"https://{link_path_parse.netloc}") or \
                link_path.startswith(f"http://{link_path_parse.netloc}"):
            download_resource(resource_path, link_path)

        else:
            download_resource(resource_path, asset_link)

        py_logger.info(f"Resource downloaded: {link_path}")

        bar.next()
    bar.finish()
