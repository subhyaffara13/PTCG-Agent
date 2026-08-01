
def skipMeta(fn):
    return skipMetaIf(True, "test doesn't work with meta tensors")(fn)

