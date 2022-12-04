import posixpath


def path_not_unique(path: str) -> bool:
    norm_path = posixpath.normpath(path)
    return (
        path != norm_path
        or norm_path == "."
        or norm_path.startswith("..")
        or norm_path.startswith("/")
    )
