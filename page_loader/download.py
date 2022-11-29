import os
import os.path
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def make_file_name_html(url):
    if url.endswith('.html'):
        url = url[:-5]
    no_scheme_url = re.search(r'(?<=//).+', url)
    url_with_dash_html = re.sub(r'[^\da-zA-Z]', '-', no_scheme_url[0])
    url_with_extension_html = f'{url_with_dash_html}.html'
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


def download_image(url, dir_name, link_path):
    # url_parse = urlparse(url)
    link_path_parse = urlparse(link_path)
    # Think about to make abspath to the second arg #
    # if link_path.startswith('/assets'):
    # print(link_path)
    if link_path.startswith('/'):
        # Make full image name
        image_name = make_file_name_image_asset(url, link_path)
        image_extension = os.path.splitext(link_path)[1]
        if image_extension == '':
            image_extension = '.html'
        image_name_with_extension = f'{image_name}{image_extension}'
        # Make image path in project
        image_path = os.path.join(dir_name, image_name_with_extension)
        # Make image name to change in HTML
        asset_local = f'{dir_name}/{image_name_with_extension}'
        # Make image path to download
        # asset_link = f'{url}{link_path}'
        asset_link = urljoin(url, link_path)
        image = requests.get(asset_link)
        # print(f"image - {image}")
        with open(image_path, 'wb') as f:
            f.write(image.content)
        return asset_local

    elif link_path.startswith(f'https://{link_path_parse.netloc}'):
        # Make full image name
        image_name = make_file_name_image_https(link_path)
        image_extension = os.path.splitext(link_path)[1]
        # print(f'image_extension = {image_extension}')
        if image_extension == '':
            image_extension = '.html'
        image_name_with_extension = f'{image_name}{image_extension}'
        image_path = os.path.join(dir_name, image_name_with_extension)
        asset_local = f'{dir_name}/{image_name_with_extension}'
        image = requests.get(link_path)
        with open(image_path, 'wb') as f:
            f.write(image.content)
        return asset_local

    else:
        return link_path


def download(url, output=os.getcwd()):
    # Making path to HTML file
    url_html = make_file_name_html(url)
    file_path = os.path.join(output, url_html)

    # Creating a directory
    dir_name = make_dir_name(url)
    dir_path = os.path.join(output, dir_name)
    os.mkdir(dir_path)

    # Getting HTML file
    response = requests.get(url)
    file = response.text

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
        # fp.write(str(soup.prettify()))

        for link in soup.find_all('link'):
            link_path = link.get('href')
            link['href'] = download_image(url, dir_name, link_path)

        for link in soup.find_all('script'):
            link_path = link.get('src')
            if link_path is not None:
                link['src'] = download_image(url, dir_name, link_path)

        fp.write(soup.prettify())

    return file_path
