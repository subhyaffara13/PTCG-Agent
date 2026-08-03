import os

def load_stdlib_py_versions(custom_typeshed_dir: str | None) -> StdlibVersions:
    """Return dict with minimum and maximum Python versions of stdlib modules.

    The contents look like
    {..., 'secrets': ((3, 6), None), 'symbol': ((2, 7), (3, 9)), ...}

    None means there is no maximum version.
    """
    typeshed_dir = custom_typeshed_dir or os_path_join(os.path.dirname(__file__), "typeshed")
    stdlib_dir = os_path_join(typeshed_dir, "stdlib")
    result = {}

    versions_path = os_path_join(stdlib_dir, "VERSIONS")
    assert os.path.isfile(versions_path), (custom_typeshed_dir, versions_path, __file__)
    with open(versions_path) as f:
        for line in f:
            line = line.split("#")[0].strip()
            if line == "":
                continue
            module, version_range = line.split(":")
            versions = version_range.split("-")
            min_version = parse_version(versions[0])
            max_version = (
                parse_version(versions[1]) if len(versions) >= 2 and versions[1].strip() else None
            )
            result[module] = min_version, max_version
    return result

