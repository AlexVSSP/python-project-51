import os.path
from page_loader.naming import make_file_name_html, make_dir_name


def make_file_path(url, output):
    url_html = make_file_name_html(url)
    file_path = os.path.join(output, url_html)
    return file_path


def make_dir_path(url, output):
    dir_name = make_dir_name(url)
    dir_path = os.path.join(output, dir_name)
    return dir_path
