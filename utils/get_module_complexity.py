
def get_module_complexity(module_path, threshold=7):
    """Returns the complexity of a module"""
    code = _read(module_path)
    return get_code_complexity(code, threshold, filename=module_path)

