
def is_optuna_available():
    return importlib.util.find_spec("optuna") is not None

