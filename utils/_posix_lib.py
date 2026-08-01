
def _posix_lib(standard_lib, libpython, early_prefix, prefix):
    if standard_lib:
        return libpython
    else:
        return os.path.join(libpython, "site-packages")

