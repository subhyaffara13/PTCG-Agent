
def skipMPS(fn):
    return skipMPSIf(True, "test doesn't work on MPS backend")(fn)

