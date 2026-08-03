import os
from typing import Callable

def resolve_class(
    qualified_class_name: str,
    package_dir: Mapping[str, str] | None = None,
    root_dir: StrPath | None = None,
) -> Callable:
    """Given a qualified class name, return the associated class object"""
    root_dir = root_dir or os.getcwd()
    idx = qualified_class_name.rfind('.')
    class_name = qualified_class_name[idx + 1 :]
    pkg_name = qualified_class_name[:idx]

    path = _find_module(pkg_name, package_dir, root_dir)
    module = _load_spec(_find_spec(pkg_name, path), pkg_name)
    return getattr(module, class_name)

