
def get_lib_version():
    try:
        libver = metadata.version("redis")
    except metadata.PackageNotFoundError:
        libver = "99.99.99"
    return libver

