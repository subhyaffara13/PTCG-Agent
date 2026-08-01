
def has_tvm() -> bool:
    try:
        importlib.import_module("tvm")
        return True
    except ImportError:
        return False

