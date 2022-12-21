import os.path
import requests
from urllib.parse import urlparse, urljoin
from page_loader.names import make_file_name_image_asset, \
    make_file_name_image_https, make_dir_name


def download_resource(url, dir_path, resource):
    link_path_parse = urlparse(url)
    # for resource in resources:
    if resource.startswith('/'):

        # Make image path in project
        image_path = os.path.join(dir_path, make_file_name_image_asset(url, resource))

        # Download resource
        asset_link = urljoin(url, resource)
        image = requests.get(asset_link)
        with open(image_path, 'wb') as f:
            f.write(image.content)

    if resource.startswith(f"https://{link_path_parse.netloc}") or \
            resource.startswith(f"http://{link_path_parse.netloc}"):

        # Make image path in project
        image_path = os.path.join(dir_path, make_file_name_image_https(resource))

        # Download resource
        image = requests.get(resource)
        with open(image_path, 'wb') as f:
            f.write(image.content)

