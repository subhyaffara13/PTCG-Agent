
def is_py_linalg_function(f: NativeFunction) -> bool:
    return f.python_module == "linalg"

