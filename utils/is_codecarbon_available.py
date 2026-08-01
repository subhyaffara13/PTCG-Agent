
def is_codecarbon_available():
    return importlib.util.find_spec("codecarbon") is not None

