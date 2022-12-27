from page_loader.naming import name_res_in_html_file
from bs4 import BeautifulSoup


# flake8: noqa: C901
def parse_resources(url, file):
    soup = BeautifulSoup(file, 'html.parser')
    tags = soup.find_all(['img', 'link', 'script'])

    resources_for_download = []
    for tag in tags:
        if tag.name == 'img':
            link_path = tag.get('src')
            if link_path is not None:
                tag['src'] = name_res_in_html_file(url, link_path)
                resources_for_download.append(link_path)
        elif tag.name == 'link':
            link_path = tag.get('href')
            if link_path is not None:
                tag['href'] = name_res_in_html_file(url, link_path)
                resources_for_download.append(link_path)
        elif tag.name == 'script':
            link_path = tag.get('src')
            if link_path is not None:
                tag['src'] = name_res_in_html_file(url, link_path)
                resources_for_download.append(link_path)
    text_result = soup.prettify()
    return resources_for_download, text_result
