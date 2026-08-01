
def is_py_fft_function(f: NativeFunction) -> bool:
    return f.python_module == "fft"

