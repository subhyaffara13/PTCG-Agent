from pathlib import Path


def is_importable(module_name: str, module_path: Path) -> bool:
    """
    Return if the given module path could be imported normally by Python, akin to the user
    entering the REPL and importing the corresponding module name directly, and corresponds
    to the module_path specified.

    :param module_name:
        Full module name that we want to check if is importable.
        For example, "app.models".

    :param module_path:
        Full path to the python module/package we want to check if is importable.
        For example, "/projects/src/app/models.py".
    """
    try:
        # Note this is different from what we do in ``_import_module_using_spec``, where we explicitly search through
        # sys.meta_path to be able to pass the path of the module that we want to import (``meta_importer.find_spec``).
        # Using importlib.util.find_spec() is different, it gives the same results as trying to import
        # the module normally in the REPL.
        spec = importlib.util.find_spec(module_name)
    except (ImportError, ValueError, ImportWarning):
        return False
    else:
        return spec_matches_module_path(spec, module_path)

