import posixpath

from edgarpy.utils.validation import path_not_unique


def test_path_not_unique():
    # NOTE: asdcasd
    assert path_not_unique("aa.bb/cc..d") == False
    assert path_not_unique("./a/b/c../d") == True
    assert path_not_unique(".") == True
    assert path_not_unique("../a/b/c") == True
    assert path_not_unique("/a/b/c") == True
