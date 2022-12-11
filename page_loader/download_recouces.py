import os.path
import requests
from urllib.parse import urlparse, urljoin
from page_loader.names import make_file_name_image_asset, \
    make_file_name_image_https


def download_image(url, dir_path, link_path):
    # link_path_parse = urlparse(link_path)
    link_path_parse = urlparse(url)
    if link_path.startswith('/'):
        # Make full image name
        image_name = make_file_name_image_asset(url, link_path)
        image_extension = os.path.splitext(link_path)[1]
        if image_extension == '':
            image_extension = '.html'
        image_name_with_extension = f"{image_name}{image_extension}"

        # Make image path in project
        image_path = os.path.join(dir_path, image_name_with_extension)
        # print(f"image_path= {image_path}")

        # # Make image name to change in HTML
        # asset_local = f"{dir_name}/{image_name_with_extension}"
        # print(f"asset_local= {asset_local}")

        # Make image path to download
        asset_link = urljoin(url, link_path)
        # print(f"asset_link= {asset_link}")
        image = requests.get(asset_link)
        with open(image_path, 'wb') as f:
            f.write(image.content)
        # return asset_local
        # return image_path
        return image_name

    if link_path.startswith(f"https://{link_path_parse.netloc}"):
        # Make full image name
        image_name = make_file_name_image_https(link_path)
        image_extension = os.path.splitext(link_path)[1]
        if image_extension == '':
            image_extension = '.html'
        image_name_with_extension = f"{image_name}{image_extension}"
        image_path = os.path.join(dir_path, image_name_with_extension)
        # asset_local = f"{dir_name}/{image_name_with_extension}"
        image = requests.get(link_path)
        with open(image_path, 'wb') as f:
            f.write(image.content)
        # return asset_local
        # return image_path
        return image_name

    else:
        return link_path
