import os
from pathlib import Path


def create_dynamic_module(name: str | os.PathLike) -> None:
    """
    Creates a dynamic module in the cache directory for modules.

    Args:
        name (`str` or `os.PathLike`):
            The name of the dynamic module to create.
    """
    init_hf_modules()
    dynamic_module_path = (Path(HF_MODULES_CACHE) / name).resolve()
    # If the parent module does not exist yet, recursively create it.
    if not dynamic_module_path.parent.exists():
        create_dynamic_module(dynamic_module_path.parent)
    os.makedirs(dynamic_module_path, exist_ok=True)
    init_path = dynamic_module_path / "__init__.py"
    if not init_path.exists():
        init_path.touch()
        # It is extremely important to invalidate the cache when we change stuff in those modules, or users end up
        # with errors about module that do not exist. Same for all other `invalidate_caches` in this file.
        importlib.invalidate_caches()

