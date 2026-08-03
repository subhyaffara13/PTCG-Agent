from pathlib import Path


def _is_namespace_package(path: Path, src_extensions: frozenset[str]) -> bool:
    if not _is_package(path):
        return False

    init_file = path / "__init__.py"
    if not init_file.exists():
        filenames = [
            filepath
            for filepath in path.iterdir()
            if filepath.suffix.lstrip(".") in src_extensions
            or filepath.name.lower() in ("setup.cfg", "pyproject.toml")
        ]
        if filenames:
            return False
    else:
        with init_file.open("rb") as open_init_file:
            file_start = open_init_file.read(4096)
            if (
                b"__import__('pkg_resources').declare_namespace(__name__)" not in file_start
                and b'__import__("pkg_resources").declare_namespace(__name__)' not in file_start
                and b"__path__ = __import__('pkgutil').extend_path(__path__, __name__)"
                not in file_start
                and b'__path__ = __import__("pkgutil").extend_path(__path__, __name__)'
                not in file_start
            ):
                return False
    return True

