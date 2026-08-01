
def is_flytekit_available():
    return importlib.util.find_spec("flytekit") is not None

