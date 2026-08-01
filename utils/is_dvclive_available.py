
def is_dvclive_available():
    return importlib.util.find_spec("dvclive") is not None

