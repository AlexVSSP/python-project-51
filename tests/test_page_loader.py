import pytest
import os
import requests_mock
import tempfile
from page_loader import download, download_image, make_dir_name, make_file_name_image_asset


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


# @pytest.fixture
# def nodejs_page_content():
#     with open("tests/fixtures/nodejs_page.html", 'rb') as f:
#         return f.read()
#
#
# def test_download_path_to_html_nodejs(nodejs_page_content):
#     with tempfile.TemporaryDirectory() as tmpdir:
#         url = 'https://page-loader.hexlet.repl.co'
#         with requests_mock.Mocker() as m:
#             m.get(url, content=nodejs_page_content)
#             download(url, tmpdir)
#         path = os.path.join(tmpdir, 'page-loader-hexlet-repl-co.html')
#         assert os.path.exists(path)
#         with open(path, 'rb') as f:
#             assert f.read() == nodejs_page_content


# @pytest.fixture
# def govuk_page_content():
#     with open("tests/fixtures/govuk_page.html", 'rb') as f:
#         return f.read()
#
#
# def test_download_path_to_html_govuk(govuk_page_content):
#     with tempfile.TemporaryDirectory() as tmpdir:
#         url = 'https://www.gov.uk'
#         with requests_mock.Mocker() as m:
#             m.get(url, content=govuk_page_content)
#             download(url, tmpdir)
#         path = os.path.join(tmpdir, 'www-gov-uk.html')
#         assert os.path.exists(path)
#         with open(path, 'rb') as f:
#             assert f.read() == govuk_page_content


def test_create_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        url = 'https://www.gov.uk'
        with requests_mock.Mocker() as m:
            m.get(url)
            download(url, tmpdir)
        expect_dir = os.path.join(tmpdir, 'www-gov-uk_files')
        assert os.path.isdir(expect_dir)


@pytest.fixture
def nodejs_page_content():
    with open("tests/fixtures/assets/page-loader-hexlet-repl-co-assets-professions-nodejs.png", 'rb') as f:
        return f.read()


def test_get_nodejs_image(nodejs_page_content):
    with tempfile.TemporaryDirectory() as tmpdir:
        url = 'https://page-loader.hexlet.repl.co/'
        link_path = '/assets/professions/nodejs.png'
        dir_name = make_dir_name(url)
        dir_path = os.path.join(tmpdir, dir_name)
        os.mkdir(dir_path)
        with requests_mock.Mocker() as m:
            m.get(link_path, content=nodejs_page_content)
            download_image(url, dir_path, link_path)  # Think about to make abspath to the second arg
        expect_dir_path = os.path.join(tmpdir, 'page-loader-hexlet-repl-co-_files')
        expect_image_path = os.path.join(expect_dir_path, 'page-loader-hexlet-repl-co-assets-professions-nodejs.png')
        assert os.path.isfile(expect_image_path)


@pytest.fixture
def nodejs_page_content_js():
    with open("tests/fixtures/assets/script.js", 'rb') as f:
        return f.read()


def test_get_nodejs_js(nodejs_page_content_js):
    with tempfile.TemporaryDirectory() as tmpdir:
        url = 'https://page-loader.hexlet.repl.co/'
        link_path = '/script.js'
        dir_name = make_dir_name(url)
        dir_path = os.path.join(tmpdir, dir_name)
        os.mkdir(dir_path)
        with requests_mock.Mocker() as m:
            m.get(link_path, content=nodejs_page_content_js)
            download_image(url, dir_path, link_path)  # Think about to make abspath to the second arg
        expect_dir_path = os.path.join(tmpdir, 'page-loader-hexlet-repl-co-_files')
        expect_image_path = os.path.join(expect_dir_path, 'page-loader-hexlet-repl-co-script.js')
        assert os.path.isfile(expect_image_path)


@pytest.fixture
def nodejs_page_content_css():
    with open("tests/fixtures/assets/application.css", 'rb') as f:
        return f.read()


def test_get_nodejs_css(nodejs_page_content_css):
    with tempfile.TemporaryDirectory() as tmpdir:
        url = 'https://page-loader.hexlet.repl.co/'
        link_path = '/assets/application.css'
        dir_name = make_dir_name(url)
        dir_path = os.path.join(tmpdir, dir_name)
        os.mkdir(dir_path)
        with requests_mock.Mocker() as m:
            m.get(link_path, content=nodejs_page_content_css)
            download_image(url, dir_path, link_path)  # Think about to make abspath to the second arg
        expect_dir_path = os.path.join(tmpdir, 'page-loader-hexlet-repl-co-_files')
        expect_image_path = os.path.join(expect_dir_path, 'page-loader-hexlet-repl-co-assets-application.css')
        assert os.path.isfile(expect_image_path)


# @pytest.fixture
# def nodejs_page_origin_content():
#     return ''
#
# def test_change_html(page_content):
#     with tempfile.TemporaryDirectory() as tmpdir:
#         result = make_file_name_image_asset('https://page-loader.hexlet.repl.co', '/assets/professions/nodejs.png')





