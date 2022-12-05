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


def make_file_name_image_asset(url, link_path):
    url_parse = urlparse(url)
    url_netloc = url_parse.netloc
    url_netloc_with_dash = re.sub(r'[^\da-zA-Z]', '-', url_netloc)

    no_extension_link_path = os.path.splitext(link_path)[0]
    link_path_with_dash = re.sub(r'[^\da-zA-Z]', '-', no_extension_link_path)
    # print(url_netloc_with_dash)
    # print(link_path_with_dash)
    file_name = f'{url_netloc_with_dash}{link_path_with_dash}'
    return file_name


def make_file_name_image_https(link_path):
    no_scheme_link_path = re.search(r'(?<=//).+', link_path)
    # print(f'site= {no_scheme_link_path[0]}')
    no_extension_link_path = os.path.splitext(no_scheme_link_path[0])
    link_path_with_dash = re.sub(r'[^\da-zA-Z]', '-', no_extension_link_path[0])
    file_name = link_path_with_dash
    return file_name
