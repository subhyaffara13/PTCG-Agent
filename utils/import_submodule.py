
def import_submodule(mod: types.ModuleType) -> None:
    """
    Ensure all the files in a given submodule are imported
    """
    for filename in sorted(os.listdir(os.path.dirname(cast(str, mod.__file__)))):
        if filename.endswith(".py") and filename[0] != "_":
            importlib.import_module(f"{mod.__name__}.{filename[:-3]}")


def import_submodule(module):
    m = __import__(module)
    for n in module.split(".")[1:]:
        m = getattr(m, n)
    return m

