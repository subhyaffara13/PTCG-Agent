
def deHexString(h):
    import binascii

    h = bytesjoin(h.split())
    return binascii.unhexlify(h)


def deHexString(hexstring):
    return eexec.deHexString(bytesjoin(hexstring.split()))

