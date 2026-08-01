
def is_swanlab_available():
    return importlib.util.find_spec("swanlab") is not None

