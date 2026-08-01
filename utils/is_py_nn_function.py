
def is_py_nn_function(f: NativeFunction) -> bool:
    return f.python_module == "nn"

