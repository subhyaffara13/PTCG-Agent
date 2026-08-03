from typing import Any

def get_dist_canonical_name(dist: importlib.metadata.Distribution) -> NormalizedName:
    """Get the distribution's normalized name.

    The ``name`` attribute is only available in Python 3.10 or later. We are
    targeting exactly that, but Mypy does not know this.
    """
    if name := parse_name_and_version_from_info_directory(dist)[0]:
        return canonicalize_name(name)

    name = cast(Any, dist).name
    if not isinstance(name, str):
        raise BadMetadata(dist, reason="invalid metadata entry 'name'")
    return canonicalize_name(name)

