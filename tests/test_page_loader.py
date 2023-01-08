import pytest
import os
import requests_mock
import tempfile
from bs4 import BeautifulSoup
from page_loader import download
from page_loader.utils.naming import make_dir_name, make_file_name_html
from page_loader.download_resources import download_resources
from page_loader.parse_resources import parse_resources
from page_loader.utils.making_paths import make_file_path, make_dir_path


@pytest.fixture
def nodejs_page_for_checks_content():
    with open("tests/fixtures/nodejs_page_for_checks.html", 'rb') as f:
        return f.read()


def test_download_path_to_html_nodejs_for_checks(nodejs_page_for_checks_content):
    with tempfile.TemporaryDirectory() as tmpdir:
        url = 'http://localhost:63342/python-project-51/tests/fixtures/nodejs_page_for_checks.html'
        with requests_mock.Mocker() as m:
            m.get(url, content=nodejs_page_for_checks_content)
            download(url, tmpdir)
        path = os.path.join(tmpdir, 'localhost-63342-python-project-51-tests-fixtures-nodejs-page-for-checks.html')
        assert os.path.exists(path)
        with open(path, 'rb') as f:
            assert f.read() == nodejs_page_for_checks_content


@pytest.fixture
def nodejs_page_content():
    with open("tests/fixtures/assets/page-loader-hexlet-repl-co-assets-professions-nodejs.png", 'rb') as f:
        return f.read()


def test_get_nodejs_image(nodejs_page_content):
    with tempfile.TemporaryDirectory() as tmpdir:
        expect_dir_path = os.path.join(tmpdir, 'page-loader-hexlet-repl-co-_files')
        expect_image_path = os.path.join(expect_dir_path, 'page-loader-hexlet-repl-co-assets-professions-nodejs.png')
        url = 'https://page-loader.hexlet.repl.co/'
        link_path = '/assets/professions/nodejs.png'
        resources = [('/assets/professions/nodejs.png', expect_image_path)]
        dir_name = make_dir_name(url)
        dir_path = os.path.join(tmpdir, dir_name)
        os.mkdir(dir_path)
        with requests_mock.Mocker() as m:
            m.get(link_path, content=nodejs_page_content)
            download_resources(url, resources)

        assert os.path.isfile(expect_image_path)


@pytest.fixture
def nodejs_page_content_js():
    with open("tests/fixtures/assets/script.js", 'rb') as f:
        return f.read()


def test_get_nodejs_js(nodejs_page_content_js):
    with tempfile.TemporaryDirectory() as tmpdir:
        expect_dir_path = os.path.join(tmpdir, 'page-loader-hexlet-repl-co-_files')
        expect_image_path = os.path.join(expect_dir_path, 'page-loader-hexlet-repl-co-script.js')
        url = 'https://page-loader.hexlet.repl.co/'
        link_path = '/script.js'
        resources = [('/script.js', expect_image_path)]
        dir_name = make_dir_name(url)
        dir_path = os.path.join(tmpdir, dir_name)
        os.mkdir(dir_path)
        with requests_mock.Mocker() as m:
            m.get(link_path, content=nodejs_page_content_js)
            download_resources(url, resources)

        assert os.path.isfile(expect_image_path)


@pytest.fixture
def nodejs_page_content_css():
    with open("tests/fixtures/assets/application.css", 'rb') as f:
        return f.read()


def test_get_nodejs_css(nodejs_page_content_css):
    with tempfile.TemporaryDirectory() as tmpdir:
        expect_dir_path = os.path.join(tmpdir, 'page-loader-hexlet-repl-co-_files')
        expect_image_path = os.path.join(expect_dir_path, 'page-loader-hexlet-repl-co-assets-application.css')
        url = 'https://page-loader.hexlet.repl.co/'
        link_path = 'https://page-loader.hexlet.repl.co/assets/application.css'
        resources = [('https://page-loader.hexlet.repl.co/assets/application.css', expect_image_path)]
        dir_name = make_dir_name(url)
        dir_path = os.path.join(tmpdir, dir_name)
        os.mkdir(dir_path)
        with requests_mock.Mocker() as m:
            m.get(link_path, content=nodejs_page_content_css)
            download_resources(url, resources)

        assert os.path.isfile(expect_image_path)


def test_exceptions():
    with tempfile.TemporaryDirectory() as tmpdir:
        url = 'https://page-loader.hexlet.repl.co/'
        url_html = make_file_name_html(url)
        file_path = os.path.join(tmpdir, url_html)
        open(file_path, "w+")
        with pytest.raises(FileExistsError):
            download(url, tmpdir)


def test_connection_error():
    with tempfile.TemporaryDirectory() as tmpdir:
        url = 'https://page-loader.hexlet.repl.co/'
        with requests_mock.Mocker() as m:
            m.get(url, status_code=404)
            with pytest.raises(ConnectionError):
                download(url, tmpdir)


@pytest.fixture
def nodejs_page_origin():
    with open("tests/fixtures/nodejs_page_origin.html", 'rb') as f:
        return f.read()


def test_parse_resources(nodejs_page_origin):
    with tempfile.TemporaryDirectory() as tmpdir:
        url = 'https://page-loader.hexlet.repl.co/'
        expect_dir_path = os.path.join(tmpdir, 'page-loader-hexlet-repl-co-_files')
        expect_resources = [('/assets/application.css', f'{tmpdir}/page-loader-hexlet-repl-co-_files/page-loader-hexlet-repl-co-assets-application.css'),
                            ('/courses', f'{tmpdir}/page-loader-hexlet-repl-co-_files/page-loader-hexlet-repl-co-courses.html'),
                            ('/assets/professions/nodejs.png', f'{tmpdir}/page-loader-hexlet-repl-co-_files/page-loader-hexlet-repl-co-assets-professions-nodejs.png'),
                            ('/script.js', f'{tmpdir}/page-loader-hexlet-repl-co-_files/page-loader-hexlet-repl-co-script.js')]
        expect_text = open('tests/fixtures/expect_text.html', 'rb')
        soup = BeautifulSoup(expect_text, 'html.parser')
        assert parse_resources(url, nodejs_page_origin, expect_dir_path) == (expect_resources, soup.prettify())


def test_making_paths():
    with tempfile.TemporaryDirectory() as tmpdir:
        url = 'https://page-loader.hexlet.repl.co/'
        output = tmpdir
        assert make_file_path(url, output) == f'{tmpdir}/page-loader-hexlet-repl-co-.html'
        assert make_dir_path(url, output) == f'{tmpdir}/page-loader-hexlet-repl-co-_files'
