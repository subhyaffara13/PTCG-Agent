
def check_halide_import() -> bool:
    """checks if we have halide available"""
    try:
        importlib.import_module("halide")
        return True
    except ModuleNotFoundError:
        return False

