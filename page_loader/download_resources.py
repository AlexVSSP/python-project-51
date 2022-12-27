import os.path
import requests
import logging
from urllib.parse import urlparse, urljoin
from page_loader.naming import name_res_start_with_asset, \
    name_res_start_with_scheme
from progress.bar import IncrementalBar


py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s "
                                 "%(message)s")

py_handler.setFormatter(py_formatter)
py_logger.addHandler(py_handler)


def download_resources(url, dir_path, resources):
    link_path_parse = urlparse(url)
    bar = IncrementalBar("Downloading resources", max=len(resources))
    for resource in resources:
        if resource.startswith('/'):

            # Make image path in project
            resource_path = os.path.join(dir_path,
                                         name_res_start_with_asset(url,
                                                                   resource))

            # Download resource
            asset_link = urljoin(url, resource)
            image = requests.get(asset_link)
            with open(resource_path, 'wb') as f:
                f.write(image.content)

        if resource.startswith(f"https://{link_path_parse.netloc}") or \
                resource.startswith(f"http://{link_path_parse.netloc}"):

            # Make image path in project
            resource_path = os.path.join(dir_path,
                                         name_res_start_with_scheme(resource))

            # Download resource
            image = requests.get(resource)
            with open(resource_path, 'wb') as f:
                f.write(image.content)
        py_logger.info(f"Resource downloaded: {resource}")
        bar.next()
    bar.finish()
