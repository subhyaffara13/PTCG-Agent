
def skipHPU(fn):
    return skipHPUIf(True, "test doesn't work on HPU backend")(fn)

