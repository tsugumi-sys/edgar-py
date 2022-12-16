from typing import Iterator, Optional, Any
import os
import sys
import hashlib
import urllib.request
import urllib.error

from tqdm import tqdm

USER_AGENT = "edgarpy"


# code refference: https://github.com/pytorch/vision/blob/main/torchvision/datasets/utils.py
def _save_response_content(
    content: Iterator[bytes],
    destination: str,
    length: Optional[int] = None,
) -> None:
    with open(destination, "wb") as fh, tqdm(total=length) as pbar:
        for chunk in content:
            if not chunk:
                continue
            fh.write(chunk)
            pbar.update(len(chunk))


# code refference: https://github.com/pytorch/vision/blob/main/torchvision/datasets/utils.py
def _urlretrieve(url: str, filename: str, chunk_size: int = 1024 * 32) -> None:
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    ) as response:
        _save_response_content(
            iter(lambda: response.read(chunk_size), b""),
            filename,
            length=response.length,
        )


def calculate_md5(fpath: str, chunk_size: int = 1024 * 1024) -> str:
    if sys.version_info >= (3, 9):
        md5 = hashlib.md5(usedforsecurity=False)  # type: ignore
    else:
        md5 = hashlib.md5()

    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            md5.update(chunk)
    return md5.hexdigest()


def check_md5(fpath: str, md5: str, **kwargs: Any) -> bool:
    return md5 == calculate_md5(fpath, **kwargs)


def check_integrity(fpath: str, md5: Optional[str] = None) -> bool:
    if not os.path.isfile(fpath):
        return False
    if md5 is None:
        return True
    return check_md5(fpath, md5)


def _get_redirect_url(url: str, max_hops: int = 3) -> str:
    initial_url = url
    headers = {"Method": "HEAD", "User-Agent": USER_AGENT}

    for _ in range(max_hops + 1):
        with urllib.request.urlopen(
            urllib.request.Request(url, headers=headers)
        ) as response:
            if response.url == url or response.url is None:
                return url
        url = response.url
    else:
        raise RecursionError(
            f"Request to {initial_url} exceeded {max_hops} redirects. The last redirect points to {url}"
        )


def download_url(
    url: str,
    root: str,
    filename: Optional[str] = None,
    md5: Optional[str] = None,
    max_redirect_hops: int = 3,
) -> None:
    """
    Download a file from url and place it in root.

    Args:
        url (str): URL to download file from
        root (str): Directory to place downloaded file in
        filename (str): Name to save the file under. If None, use the basename of the URL
        md5 (str, optional): MD5 checksum of the download. If None, do not check.
        max_redirect_hops (int): Maximum number of redirect hops allowed.
    """
    root = os.path.expanduser(root)
    if not filename:
        filename = os.path.basename(url)
    fpath = os.path.join(root, filename)

    os.makedirs(root, exist_ok=True)

    if check_integrity(fpath, md5):
        print("Using downloaded and verified file: " + fpath)
        return

    url = _get_redirect_url(url, max_hops=max_redirect_hops)

    try:
        print("Downloading " + url + " to " + fpath)
        _urlretrieve(url, fpath)
    except (urllib.error.URLError, OSError) as e:
        if url[:5] == "https":
            url = url.replace("https:", "http:")
            print(
                "Failed downloaded. Trying https -> http instead. Downloading "
                + url
                + " to "
                + fpath
            )
            _urlretrieve(url, fpath)
        else:
            raise e

    if not check_integrity(fpath, md5):
        raise RuntimeError("File not found or corrupted.")
