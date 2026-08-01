
def _get_package_root(package_name: str, directory_name: str | None = None):
    from importlib.metadata import PackageNotFoundError, distribution  # noqa: PLC0415

    root_directory_name = directory_name or package_name
    try:
        dist = distribution(package_name)
        files = dist.files or []

        for file in files:
            if file.name.endswith("__init__.py") and root_directory_name in file.parts:
                return file.locate().parent

        # Fallback to the first __init__.py
        if not directory_name:
            for file in files:
                if file.name.endswith("__init__.py"):
                    return file.locate().parent
    except PackageNotFoundError:
        # package not found, do nothing
        pass

    return None

