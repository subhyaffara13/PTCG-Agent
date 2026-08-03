import sys
from pathlib import Path


def get_typeshed_stdlib_modules(
    custom_typeshed_dir: str | None, version_info: tuple[int, int] | None = None
) -> set[str]:
    """Returns a list of stdlib modules in typeshed (for current Python version)."""
    stdlib_py_versions = mypy.modulefinder.load_stdlib_py_versions(custom_typeshed_dir)
    if version_info is None:
        version_info = sys.version_info[0:2]

    def exists_in_version(module: str) -> bool:
        assert version_info is not None
        parts = module.split(".")
        for i in range(len(parts), 0, -1):
            current_module = ".".join(parts[:i])
            if current_module in stdlib_py_versions:
                minver, maxver = stdlib_py_versions[current_module]
                return version_info >= minver and (maxver is None or version_info <= maxver)
        return False

    if custom_typeshed_dir:
        typeshed_dir = Path(custom_typeshed_dir)
    else:
        typeshed_dir = Path(mypy.build.default_data_dir()) / "typeshed"
    stdlib_dir = typeshed_dir / "stdlib"

    modules: set[str] = set()
    for path in stdlib_dir.rglob("*.pyi"):
        if path.stem == "__init__":
            path = path.parent
        module = ".".join(path.relative_to(stdlib_dir).parts[:-1] + (path.stem,))
        if exists_in_version(module):
            modules.add(module)
    return modules

