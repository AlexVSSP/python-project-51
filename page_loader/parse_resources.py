from page_loader.naming import make_resource_name_in_html_file


# flake8: noqa: C901
def parse_resources(url, tags):
    resources_for_download = []
    for tag in tags:
        if tag.name == 'img':
            link_path = tag.get('src')
            if link_path is not None:
                tag['src'] = make_resource_name_in_html_file(url, link_path)
                resources_for_download.append(link_path)
        elif tag.name == 'link':
            link_path = tag.get('href')
            if link_path is not None:
                tag['href'] = make_resource_name_in_html_file(url, link_path)
                resources_for_download.append(link_path)
        elif tag.name == 'script':
            link_path = tag.get('src')
            if link_path is not None:
                tag['src'] = make_resource_name_in_html_file(url, link_path)
                resources_for_download.append(link_path)
    return resources_for_download
