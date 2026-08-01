
def _module_dir(m: types.ModuleType) -> str | None:
    # Protect against a module not exporting __file__ - this can happen for
    # frozen modules, for example.
    file = getattr(m, "__file__", None)
    return file and _strip_init_py(file)

