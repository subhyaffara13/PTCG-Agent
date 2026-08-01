
def flags2names(flags):
    info = []
    for flagname in [
            "CONTIGUOUS",
            "FORTRAN",
            "OWNDATA",
            "ENSURECOPY",
            "ENSUREARRAY",
            "ALIGNED",
            "NOTSWAPPED",
            "WRITEABLE",
            "WRITEBACKIFCOPY",
            "UPDATEIFCOPY",
            "BEHAVED",
            "BEHAVED_RO",
            "CARRAY",
            "FARRAY",
    ]:
        if abs(flags) & getattr(wrap, flagname, 0):
            info.append(flagname)
    return info

