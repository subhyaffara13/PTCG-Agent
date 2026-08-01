
def clone_module(mod_name: str, globals_: dict[str, object]) -> list[str]:
    """Import everything from module, updating globals().
    Returns __all__.
    """
    mod = importlib.import_module(mod_name)
    # Neither of these two methods is sufficient by itself,
    # depending on various idiosyncrasies of the libraries we're wrapping.
    objs = {}
    exec(f"from {mod.__name__} import *", objs)

    for n in dir(mod):
        if not n.startswith("_") and hasattr(mod, n):
            objs[n] = getattr(mod, n)

    globals_.update(objs)
    return list(objs)

