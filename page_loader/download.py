import os.path
import requests
import re


def download(url, output=os.getcwd()):
    no_extension_url = os.path.splitext(url)[0]  # [0] - filepath before dot
    # [1]- is extension, which is going after dot
    no_scheme_url = re.search(r'(?<=//).+', no_extension_url)
    url_with_dash = re.sub(r'[^\da-zA-Z]', '-', no_scheme_url[0])
    url_with_extension = f'{url_with_dash}.html'
    file_path = os.path.join(output, url_with_extension)

    response = requests.get(url)
    with open(file_path, 'w+') as fp:
        fp.write(response.text)

    return file_path
