
def _register_py_impl_temporarily(op_overload, key, fn):
    try:
        op_overload.py_impl(key)(fn)
        yield
    finally:
        del op_overload.py_kernels[key]
        op_overload._dispatch_cache.clear()

