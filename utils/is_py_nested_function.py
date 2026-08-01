
def is_py_nested_function(f: NativeFunction) -> bool:
    return f.python_module == "nested"

