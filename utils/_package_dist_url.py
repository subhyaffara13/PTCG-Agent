import os

def _package_dist_url(
    pylock_path_or_url: str, path: str | None, url: str | None
) -> str:
    """Compute an url from a Pylock package path and url.

    Give priority to path over url. If path is relative,
    compute an url using the pylock file location as base.
    """
    if path is not None:
        if not os.path.isabs(path):
            # relative path, join to pylock location
            if _is_url(pylock_path_or_url):
                return urljoin(pylock_path_or_url, path)
            else:
                return path_to_url(
                    os.path.join(os.path.dirname(pylock_path_or_url), path)
                )
        else:
            # absolute path, reject if pylock comes from a URL
            if _is_url(pylock_path_or_url):
                raise InstallationError(
                    f"Absolute paths are not supported in pylock files obtained "
                    f"from a URL: {path!r} in {pylock_path_or_url!r}"
                )
            return path_to_url(path)
    else:
        assert url is not None  # guaranteed by packaging.pylock validation
        return url

