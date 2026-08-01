
def get_typecache(backend):
    # returns _typecache_cffi_backend if backend is the _cffi_backend
    # module, or type(backend).__typecache if backend is an instance of
    # CTypesBackend (or some FakeBackend class during tests)
    if isinstance(backend, types.ModuleType):
        return _typecache_cffi_backend
    with global_lock:
        if not hasattr(type(backend), '__typecache'):
            type(backend).__typecache = weakref.WeakValueDictionary()
        return type(backend).__typecache

