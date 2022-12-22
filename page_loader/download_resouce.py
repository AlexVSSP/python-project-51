import os.path
import requests
from urllib.parse import urlparse, urljoin
from page_loader.naming import name_res_start_with_asset, \
    name_res_start_with_scheme


def download_resource(url, dir_path, resource):
    link_path_parse = urlparse(url)
    # for resource in resources:
    if resource.startswith('/'):

        # Make image path in project
        resource_path = os.path.join(dir_path,
                                     name_res_start_with_asset(url, resource))

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
