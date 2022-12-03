import posixpath

from edgarpy.utils.validation import path_not_unique


def test_path_not_unique():
    assert path_not_unique("a/b/c") == False
    assert path_not_unique("./a/b/c") == True
    assert path_not_unique("./a/b/../d") == True
    assert path_not_unique(".") == True
    assert path_not_unique("../a/b/c") == True
    assert path_not_unique("/a/b/c") == True
