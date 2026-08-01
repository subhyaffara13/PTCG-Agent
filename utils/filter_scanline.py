
def filter_scanline(type, line, fo, prev=None):
    """Apply a scanline filter to a scanline.  `type` specifies the
    filter type (0 to 4); `line` specifies the current (unfiltered)
    scanline as a sequence of bytes; `prev` specifies the previous
    (unfiltered) scanline as a sequence of bytes. `fo` specifies the
    filter offset; normally this is size of a pixel in bytes (the number
    of bytes per sample times the number of channels), but when this is
    < 1 (for bit depths < 8) then the filter offset is 1.
    """

    assert 0 <= type < 5

    # The output array.  Which, pathetically, we extend one-byte at a
    # time (fortunately this is linear).
    out = array("B", [type])

    def sub():
        ai = -fo
        for x in line:
            if ai >= 0:
                x = (x - line[ai]) & 0xFF
            out.append(x)
            ai += 1

    def up():
        for i, x in enumerate(line):
            x = (x - prev[i]) & 0xFF
            out.append(x)

    def average():
        ai = -fo
        for i, x in enumerate(line):
            if ai >= 0:
                x = (x - ((line[ai] + prev[i]) >> 1)) & 0xFF
            else:
                x = (x - (prev[i] >> 1)) & 0xFF
            out.append(x)
            ai += 1

    def paeth():
        # http://www.w3.org/TR/PNG/#9Filter-type-4-Paeth
        ai = -fo  # also used for ci
        for i, x in enumerate(line):
            a = 0
            b = prev[i]
            c = 0

            if ai >= 0:
                a = line[ai]
                c = prev[ai]
            p = a + b - c
            pa = abs(p - a)
            pb = abs(p - b)
            pc = abs(p - c)
            if pa <= pb and pa <= pc:
                Pr = a
            elif pb <= pc:
                Pr = b
            else:
                Pr = c

            x = (x - Pr) & 0xFF
            out.append(x)
            ai += 1

    if not prev:
        # We're on the first line.  Some of the filters can be reduced
        # to simpler cases which makes handling the line "off the top"
        # of the image simpler.  "up" becomes "none"; "paeth" becomes
        # "left" (non-trivial, but true). "average" needs to be handled
        # specially.
        if type == 2:  # "up"
            return line  # type = 0
        elif type == 3:
            prev = [0] * len(line)
        elif type == 4:  # "paeth"
            type = 1
    if type == 0:
        out.extend(line)
    elif type == 1:
        sub()
    elif type == 2:
        up()
    elif type == 3:
        average()
    else:  # type == 4
        paeth()
    return out

