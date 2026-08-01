
def _is_setuptools_namespace(location: pathlib.Path) -> bool:
    try:
        with open(location / "__init__.py", "rb") as stream:
            data = stream.read(4096)
    except OSError:
        return False
    extend_path = b"pkgutil" in data and b"extend_path" in data
    declare_namespace = (
        b"pkg_resources" in data and b"declare_namespace(__name__)" in data
    )
    return extend_path or declare_namespace

