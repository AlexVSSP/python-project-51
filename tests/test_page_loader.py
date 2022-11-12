import pytest
import os
import requests_mock
from page_loader import download
import tempfile


@pytest.fixture
def page_content():
    with open("tests/fixtures/page_code.html") as f:
        return f.read()


def test_download_path_to_html(page_content):
    with tempfile.TemporaryDirectory() as tmpdir:
        url = 'https://ru.hexlet.io/courses'
        with requests_mock.Mocker() as m:
            m.get(url, text=page_content)
            download(url, tmpdir)
        path = f'{tmpdir}/ru-hexlet-io-courses.html'
        assert os.path.exists(path)
        with open(path) as f:
            assert f.read() == page_content
