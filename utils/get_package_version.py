
def get_package_version(package_name: str):
    try:
        return version(package_name)
    except PackageNotFoundError:
        return None

