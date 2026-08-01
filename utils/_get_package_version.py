
def _get_package_version(package_name: str):
    from importlib.metadata import PackageNotFoundError, version  # noqa: PLC0415

    try:
        package_version = version(package_name)
    except PackageNotFoundError:
        package_version = None
    return package_version

