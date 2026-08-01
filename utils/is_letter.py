
def isLetter(ch: int) -> bool:
    lc = ch | 0x20  # to lower case
    # /* a */ and /* z */
    return (lc >= 0x61) and (lc <= 0x7A)

