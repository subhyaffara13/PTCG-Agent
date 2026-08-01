
def _is_builtin_module(module):
    if not hasattr(module, "__file__"): return True
    if module.__file__ is None: return False
    # If a module file name starts with prefix, it should be a builtin
    # module, so should always be pickled as a reference.
    names = ["base_prefix", "base_exec_prefix", "exec_prefix", "prefix", "real_prefix"]
    rp = os.path.realpath
    # See https://github.com/uqfoundation/dill/issues/566
    return (
        any(
            module.__file__.startswith(getattr(sys, name))
            or rp(module.__file__).startswith(rp(getattr(sys, name)))
            for name in names
            if hasattr(sys, name)
        )
        or module.__file__.endswith(EXTENSION_SUFFIXES)
        or 'site-packages' in module.__file__
    )

