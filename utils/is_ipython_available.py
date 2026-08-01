
def is_ipython_available() -> bool:
    return importlib.util.find_spec("IPython") is not None

