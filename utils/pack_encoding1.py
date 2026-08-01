
def packEncoding1(charset, encoding, strings):
    fmt = 1
    m = {}
    for code in range(len(encoding)):
        name = encoding[code]
        if name != ".notdef":
            m[name] = code
    ranges = []
    first = None
    end = 0
    for name in charset[1:]:
        code = m.get(name, -1)
        if first is None:
            first = code
        elif end + 1 != code:
            nLeft = end - first
            ranges.append((first, nLeft))
            first = code
        end = code
    nLeft = end - first
    ranges.append((first, nLeft))

    # remove unencoded glyphs at the end.
    while ranges and ranges[-1][0] == -1:
        ranges.pop()

    data = [packCard8(fmt), packCard8(len(ranges))]
    for first, nLeft in ranges:
        if first == -1:  # unencoded
            first = 0
        data.append(packCard8(first) + packCard8(nLeft))
    return bytesjoin(data)

