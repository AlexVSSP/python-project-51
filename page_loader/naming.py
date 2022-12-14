import re
import os.path
from urllib.parse import urlparse


def make_file_name_html(url):
    if url.endswith('.html'):
        url = url[:-5]
    no_scheme_url = re.search(r'(?<=//).+', url)
    url_with_dash_html = re.sub(r'[^\da-zA-Z]', '-', no_scheme_url[0])
    url_with_extension_html = f"{url_with_dash_html}.html"
    return url_with_extension_html


def make_dir_name(url):
    if url.endswith('.html'):
        url = url[:-5]
    no_scheme_url = re.search(r'(?<=//).+', url)
    dir_name_with_dash = re.sub(r'[^\da-zA-Z]', '-', no_scheme_url[0])
    dir_name = f'{dir_name_with_dash}_files'
    return dir_name


def name_res_start_with_asset(url, link_path):
    url_parse = urlparse(url)
    url_netloc = url_parse.netloc
    url_netloc_with_dash = re.sub(r'[^\da-zA-Z]', '-', url_netloc)

    no_extension_link_path = os.path.splitext(link_path)[0]
    link_path_with_dash = re.sub(r'[^\da-zA-Z]', '-', no_extension_link_path)
    resource_name = f'{url_netloc_with_dash}{link_path_with_dash}'

    resource_extension = os.path.splitext(link_path)[1]
    if resource_extension == '':
        resource_extension = '.html'
    resource_name_with_extension = f"{resource_name}{resource_extension}"
    return resource_name_with_extension


def name_res_start_with_scheme(link_path):
    no_scheme_link_path = re.search(r'(?<=//).+', link_path)
    no_extension_link_path = os.path.splitext(no_scheme_link_path[0])
    link_path_with_dash = re.sub(r'[^\da-zA-Z]', '-', no_extension_link_path[0])
    resource_name = link_path_with_dash

    resource_extension = os.path.splitext(link_path)[1]
    if resource_extension == '':
        resource_extension = '.html'
    resource_name_with_extension = f"{resource_name}{resource_extension}"
    return resource_name_with_extension


def name_res_in_html_file(url, link_path):
    link_path_parse = urlparse(url)
    if link_path.startswith('/'):

        # Make full image name
        resource_name_with_extension = name_res_start_with_asset(url, link_path)

        # Make image name to change in HTML
        dir_name = make_dir_name(url)
        asset_local = f"{dir_name}/{resource_name_with_extension}"
        return asset_local

    if link_path.startswith(f"https://{link_path_parse.netloc}") or \
            link_path.startswith(f"http://{link_path_parse.netloc}"):

        # Make full image name
        resource_name_with_extension = name_res_start_with_scheme(link_path)

        # Make image name to change in HTML
        dir_name = make_dir_name(url)
        asset_local = f"{dir_name}/{resource_name_with_extension}"
        return asset_local

    else:
        return link_path
