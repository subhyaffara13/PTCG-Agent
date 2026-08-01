
def is_flute_available() -> bool:
    is_available, flute_version = _is_package_available("flute", return_version=True)
    return is_available and version.parse(flute_version) >= version.parse("0.4.1")

