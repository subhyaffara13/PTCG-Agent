
def jit_module_from_flatbuffer(f):
    if isinstance(f, (str, os.PathLike)):
        f = os.fspath(f)
        return wrap_cpp_module(torch._C._load_jit_module_from_file(f))
    else:
        return wrap_cpp_module(torch._C._load_jit_module_from_bytes(f.read()))

