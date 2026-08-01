
def skipPRIVATEUSE1(fn):
    return skipPRIVATEUSE1If(True, "test doesn't work on privateuse1 backend")(fn)

