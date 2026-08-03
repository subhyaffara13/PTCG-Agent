import os
import sys
from pathlib import Path


def get_class_in_module(
    class_name: str,
    module_path: str | os.PathLike,
    *,
    force_reload: bool = False,
) -> type:
    """
    Import a module on the cache directory for modules and extract a class from it.

    Args:
        class_name (`str`): The name of the class to import.
        module_path (`str` or `os.PathLike`): The path to the module to import.
        force_reload (`bool`, *optional*, defaults to `False`):
            Whether to reload the dynamic module from file if it already exists in `sys.modules`.
            Otherwise, the module is only reloaded if the file has changed.

    Returns:
        `typing.Type`: The class looked for.
    """
    name = os.path.normpath(module_path)
    name = name.removesuffix(".py")
    name = name.replace(os.path.sep, ".")
    module_file: Path = Path(HF_MODULES_CACHE) / module_path
    with _HF_REMOTE_CODE_LOCK:
        if force_reload:
            sys.modules.pop(name, None)
            importlib.invalidate_caches()
        cached_module: ModuleType | None = sys.modules.get(name)
        module_spec = importlib.util.spec_from_file_location(name, location=module_file)

        # Hash the module file and all its relative imports to check if we need to reload it
        module_files: list[Path] = [module_file] + sorted(map(Path, get_relative_import_files(module_file)))
        module_hash: str = hashlib.sha256(b"".join(bytes(f) + f.read_bytes() for f in module_files)).hexdigest()

        module: ModuleType
        if cached_module is None:
            module = importlib.util.module_from_spec(module_spec)
            # insert it into sys.modules before any loading begins
            sys.modules[name] = module
        else:
            module = cached_module
        # reload in both cases, unless the module is already imported and the hash hits
        if getattr(module, "__transformers_module_hash__", "") != module_hash:
            module_spec.loader.exec_module(module)
            module.__transformers_module_hash__ = module_hash
        return getattr(module, class_name)

