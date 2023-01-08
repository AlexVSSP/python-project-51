import os.path
from page_loader.utils.naming import name_res_in_html_file
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_loader.utils.naming import name_res_start_with_asset, \
    name_res_start_with_scheme


REQUIRED_RESOURCES = {'img': 'src', 'link': 'href', 'script': 'src'}


# flake8: noqa: C901
def parse_resources(url, file, dir_path):
    soup = BeautifulSoup(file, 'html.parser')
    tags = soup.find_all(REQUIRED_RESOURCES)

    resources_for_download = []
    for tag in tags:
        attr = REQUIRED_RESOURCES[tag.name]
        link_path = tag.get(attr)
        if link_path is not None:
            tag[attr] = name_res_in_html_file(url, link_path)
            link_path_parse = urlparse(url)

            if link_path.startswith(f"https://{link_path_parse.netloc}") or \
                    link_path.startswith(f"http://{link_path_parse.netloc}"):
                resource_path = os.path.join(dir_path,
                                             name_res_start_with_scheme(link_path))
                resources_for_download.append((link_path, resource_path))
            if link_path.startswith('/'):
                resource_path = os.path.join(dir_path,
                                             name_res_start_with_asset(url,
                                                                       link_path))
                resources_for_download.append((link_path, resource_path))

    text_result = soup.prettify()

    return resources_for_download, text_result
