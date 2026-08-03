from typing import Callable

def cmdclass(
    values: dict[str, str],
    package_dir: Mapping[str, str] | None = None,
    root_dir: StrPath | None = None,
) -> dict[str, Callable]:
    """Given a dictionary mapping command names to strings for qualified class
    names, apply :func:`resolve_class` to the dict values.
    """
    return {k: resolve_class(v, package_dir, root_dir) for k, v in values.items()}

