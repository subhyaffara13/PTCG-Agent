
def is_py_special_function(f: NativeFunction) -> bool:
    return f.python_module == "special"

