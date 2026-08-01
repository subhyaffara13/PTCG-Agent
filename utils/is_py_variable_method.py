
def is_py_variable_method(f: NativeFunction) -> bool:
    return f.python_module is None and Variant.method in f.variants

