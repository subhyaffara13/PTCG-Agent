import sys

def insert_missing_modules(modules: dict[str, ModuleType], module_name: str) -> None:
    """
    Used by ``import_path`` to create intermediate modules when using mode=importlib.

    When we want to import a module as "src.tests.test_foo" for example, we need
    to create empty modules "src" and "src.tests" after inserting "src.tests.test_foo",
    otherwise "src.tests.test_foo" is not importable by ``__import__``.
    """
    module_parts = module_name.split(".")
    while module_name:
        parent_module_name, _, child_name = module_name.rpartition(".")
        if parent_module_name:
            parent_module = modules.get(parent_module_name)
            if parent_module is None:
                try:
                    # If sys.meta_path is empty, calling import_module will issue
                    # a warning and raise ModuleNotFoundError. To avoid the
                    # warning, we check sys.meta_path explicitly and raise the error
                    # ourselves to fall back to creating a dummy module.
                    if not sys.meta_path:
                        raise ModuleNotFoundError
                    parent_module = importlib.import_module(parent_module_name)
                except ModuleNotFoundError:
                    parent_module = ModuleType(
                        module_name,
                        doc="Empty module created by pytest's importmode=importlib.",
                    )
                modules[parent_module_name] = parent_module

            # Add child attribute to the parent that can reference the child
            # modules.
            if not hasattr(parent_module, child_name):
                setattr(parent_module, child_name, modules[module_name])

        module_parts.pop(-1)
        module_name = ".".join(module_parts)

