
def skipLazy(fn):
    return skipLazyIf(True, "test doesn't work with lazy tensors")(fn)

