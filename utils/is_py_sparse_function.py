
def is_py_sparse_function(f: NativeFunction) -> bool:
    return f.python_module == "sparse"

