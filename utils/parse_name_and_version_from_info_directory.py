import os

def parse_name_and_version_from_info_directory(
    dist: importlib.metadata.Distribution,
) -> tuple[str | None, str | None]:
    """Get a name and version from the metadata directory name.

    This is much faster than reading distribution metadata.
    """
    info_location = get_info_location(dist)
    if info_location is None:
        return None, None

    stem, suffix = os.path.splitext(info_location.name)
    if suffix == ".dist-info":
        name, sep, version = stem.partition("-")
        if sep:
            return name, version

    if suffix == ".egg-info":
        name = stem.split("-", 1)[0]
        return name, None

    return None, None

