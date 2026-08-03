import sys

def clear_import_cache() -> None:
    """
    Clear cached Transformers modules to allow reloading modified code.

    This is useful when actively developing/modifying Transformers code.
    """
    # Get all transformers modules
    transformers_modules = [mod_name for mod_name in sys.modules if mod_name.startswith("transformers.")]

    # Remove them from sys.modules
    for mod_name in transformers_modules:
        module = sys.modules[mod_name]
        # Clear _LazyModule caches if applicable
        if isinstance(module, _LazyModule):
            module._objects = {}  # Clear cached objects
        del sys.modules[mod_name]

    # Force reload main transformers module
    if "transformers" in sys.modules:
        main_module = sys.modules["transformers"]
        if isinstance(main_module, _LazyModule):
            main_module._objects = {}  # Clear cached objects
        importlib.reload(main_module)

