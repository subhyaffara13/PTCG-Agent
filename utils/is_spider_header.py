
def isSpiderHeader(t: tuple[float, ...]) -> int:
    h = (99,) + t  # add 1 value so can use spider header index start=1
    # header values 1,2,5,12,13,22,23 should be integers
    for i in [1, 2, 5, 12, 13, 22, 23]:
        if not isInt(h[i]):
            return 0
    # check iform
    iform = int(h[5])
    if iform not in iforms:
        return 0
    # check other header values
    labrec = int(h[13])  # no. records in file header
    labbyt = int(h[22])  # total no. of bytes in header
    lenbyt = int(h[23])  # record length in bytes
    if labbyt != (labrec * lenbyt):
        return 0
    # looks like a valid header
    return labbyt

