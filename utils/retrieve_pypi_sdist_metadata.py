
def retrieve_pypi_sdist_metadata(package, version):
    # https://warehouse.pypa.io/api-reference/json.html
    id_ = package if version is LATEST else f"{package}/{version}"
    with urlopen(f"https://pypi.org/pypi/{id_}/json") as f:
        metadata = json.load(f)

    if metadata["info"]["yanked"]:
        raise ValueError(f"Release for {package} {version} was yanked")

    version = metadata["info"]["version"]
    release = metadata["releases"][version] if version is LATEST else metadata["urls"]
    (sdist,) = filter(lambda d: d["packagetype"] == "sdist", release)
    return sdist

