
def enable_reentrant_dispatch():
    # NB: this can't simply be
    # `enable_reentrant_dispatch = torch._C._RestorePythonTLSSnapshot`
    # because:
    # 1. torch._C._RestorePythonTLSSnapshot is unavailable when this file
    #    initially gets imported. Probably an import order thing.
    # 2. enable_reentrant_dispatch is technically public API; assigning
    #    it the object would change the __module__ to look private.
    with torch._C._RestorePythonTLSSnapshot():
        try:
            yield
        finally:
            pass

