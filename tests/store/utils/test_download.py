from typing import Optional
import os
from tempfile import NamedTemporaryFile, TemporaryDirectory
import contextlib
import string
import random

import pytest

from edgarpy.store.utils import download

random.seed(1234)


def get_random_string(length: int = 10000):
    letters = string.ascii_lowercase
    res = "".join(random.choice(letters) for i in range(length))
    return res


dummy_text = get_random_string()

TEST_FILE = NamedTemporaryFile()
TEST_FILE.write(dummy_text.encode("ascii"))
correct_md5 = "674d8c2354ababb44e1fdab5c2e83faa"


def patch_response(mocker):
    class Response:
        def __init__(self, url: str = "https://url.org"):
            self.url = url
            self.data = TEST_FILE

        def read(self, chunk_size: int = 1024) -> bytes:
            return self.data.read(chunk_size)

        @property
        def length(self):
            return os.stat(self.data.name).st_size

    @contextlib.contextmanager
    def patched_opener(*args, **kwargs):
        yield Response()

    return mocker.patch(
        "edgarpy.store.utils.download.urllib.request.urlopen",
        side_effect=patched_opener,
    )


def test_urlretrieve(mocker):
    url = "https://url.org/example.json"
    expected_redirect_url = "https//csdc/example.json"
    mock = patch_response(mocker)
    tmp_dir = TemporaryDirectory()
    filename = os.path.join(tmp_dir.name, "exanmple.json")
    download._urlretrieve(url, filename)
    assert os.path.exists(filename)


def test_check_md5():
    wrong_md5 = ""
    correct_md5 = "674d8c2354ababb44e1fdab5c2e83faa"
    assert download.check_md5(TEST_FILE.name, correct_md5)
    assert not download.check_md5(TEST_FILE.name, wrong_md5)


def test_check_integrity():
    nonexising_path = ""
    correct_md5 = "674d8c2354ababb44e1fdab5c2e83faa"
    wrong_md5 = ""
    assert download.check_integrity(TEST_FILE.name, correct_md5)
    assert download.check_integrity(TEST_FILE.name)
    assert not download.check_integrity(nonexising_path)
    assert not download.check_integrity(TEST_FILE.name, wrong_md5)


def patch_url_redirection(mocker, redirect_url):
    class Response:
        def __init__(self, url):
            self.url = url

    @contextlib.contextmanager
    def patched_opener(*args, **kwargs):
        yield Response(redirect_url)

    return mocker.patch(
        "edgarpy.store.utils.download.urllib.request.urlopen",
        side_effect=patched_opener,
    )


def test_get_redirect_url(mocker):
    url = "https://url.org"
    expected_redirect_url = "https://redirect.url.org"
    mock = patch_url_redirection(mocker, expected_redirect_url)
    actual = download._get_redirect_url(url)
    assert actual == expected_redirect_url

    assert mock.call_count == 2
    call_args1, call_args2 = mock.call_args_list
    assert call_args1[0][0].full_url == url
    assert call_args2[0][0].full_url == expected_redirect_url


def test_get_redirect_url_max_hops_exceeded(mocker):
    url = "https://url.org"
    redirect_url = "https://redirect.url.org"

    mock = patch_url_redirection(mocker, redirect_url)

    with pytest.raises(RecursionError):
        download._get_redirect_url(url, max_hops=0)

    assert mock.call_count == 1
    assert mock.call_args[0][0].full_url == url
