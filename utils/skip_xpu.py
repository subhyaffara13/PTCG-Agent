
def skipXPU(fn):
    return skipXPUIf(True, "test doesn't work on XPU backend")(fn)

