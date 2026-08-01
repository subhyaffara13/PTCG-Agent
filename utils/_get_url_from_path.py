
def _get_url_from_path(path: str, name: str) -> Optional[str]:
    """
    First, it checks whether a provided path looks like a path. If it
    is, returns the path.

    Otherwise, check if the path is notan archive file (such as a .whl) or is a
    PEP 508 URL "name@url" requirement and return None
    """
    if not (path and name):
        return

    if _looks_like_path(name):
        return path

    if not is_archive_file(path):
        return None

    if is_name_at_url_requirement(name) or is_name_at_url_requirement(path):
        return None

    return path


def _get_url_from_path(path, name):
    if _looks_like_path(name) and os.path.isdir(path):
        if _is_installable_dir(path):
            return _path_to_url(path)
        # TODO: The is_installable_dir test here might not be necessary
        #       now that it is done in load_pyproject_toml too.
        raise PipError(
            f"Directory {name!r} is not installable. Neither 'setup.py' "
            "nor 'pyproject.toml' found."
        )
    if not _is_archive_file(path):
        return None
    if os.path.isfile(path):
        return _path_to_url(path)
    urlreq_parts = name.split("@", 1)
    if len(urlreq_parts) >= 2 and not _looks_like_path(urlreq_parts[0]):
        # If the path contains '@' and the part before it does not look
        # like a path, try to treat it as a PEP 440 URL req instead.
        return None
    return _path_to_url(path)


def _get_url_from_path(path: str, name: str) -> str | None:
    """
    First, it checks whether a provided path is an installable directory. If it
    is, returns the path.

    If false, check if the path is an archive file (such as a .whl).
    The function checks if the path is a file. If false, if the path has
    an @, it will treat it as a PEP 440 URL requirement and return the path.
    """
    if _looks_like_path(name) and os.path.isdir(path):
        if is_installable_dir(path):
            return path_to_url(path)
        # TODO: The is_installable_dir test here might not be necessary
        #       now that it is done in load_pyproject_toml too.
        raise InstallationError(
            f"Directory {name!r} is not installable. Neither 'setup.py' "
            "nor 'pyproject.toml' found."
        )
    if not is_archive_file(path):
        return None
    if os.path.isfile(path):
        return path_to_url(path)
    urlreq_parts = name.split("@", 1)
    if len(urlreq_parts) >= 2 and not _looks_like_path(urlreq_parts[0]):
        # If the path contains '@' and the part before it does not look
        # like a path, try to treat it as a PEP 440 URL req instead.
        return None
    logger.warning(
        "Requirement %r looks like a filename, but the file does not exist",
        name,
    )
    return path_to_url(path)

