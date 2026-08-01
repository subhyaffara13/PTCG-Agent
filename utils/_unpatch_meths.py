
def _unpatch_meths(patchlist):
    for cls, name, old_meth in reversed(patchlist):
        setattr(cls, name, old_meth)

