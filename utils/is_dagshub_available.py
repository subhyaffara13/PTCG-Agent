
def is_dagshub_available():
    return None not in [importlib.util.find_spec("dagshub"), importlib.util.find_spec("mlflow")]

