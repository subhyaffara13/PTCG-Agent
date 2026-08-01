
def load_xbm(curs, mask):
    """pygame.cursors.load_xbm(cursorfile, maskfile) -> cursor_args
    reads a pair of XBM files into set_cursor arguments

    Arguments can either be filenames or filelike objects
    with the readlines method. Not largely tested, but
    should work with typical XBM files.
    """

    def bitswap(num):
        val = 0
        for x in range(8):
            b = num & (1 << x) != 0
            val = val << 1 | b
        return val

    if hasattr(curs, "readlines"):
        curs = curs.readlines()
    else:
        with open(curs, encoding="ascii") as cursor_f:
            curs = cursor_f.readlines()

    if hasattr(mask, "readlines"):
        mask = mask.readlines()
    else:
        with open(mask, encoding="ascii") as mask_f:
            mask = mask_f.readlines()

    # avoid comments
    for i, line in enumerate(curs):
        if line.startswith("#define"):
            curs = curs[i:]
            break

    for i, line in enumerate(mask):
        if line.startswith("#define"):
            mask = mask[i:]
            break

    # load width,height
    width = int(curs[0].split()[-1])
    height = int(curs[1].split()[-1])
    # load hotspot position
    if curs[2].startswith("#define"):
        hotx = int(curs[2].split()[-1])
        hoty = int(curs[3].split()[-1])
    else:
        hotx = hoty = 0

    info = width, height, hotx, hoty

    possible_starts = ("static char", "static unsigned char")
    for i, line in enumerate(curs):
        if line.startswith(possible_starts):
            break
    data = " ".join(curs[i + 1 :]).replace("};", "").replace(",", " ")
    cursdata = tuple(bitswap(int(x, 16)) for x in data.split())
    for i, line in enumerate(mask):
        if line.startswith(possible_starts):
            break
    data = " ".join(mask[i + 1 :]).replace("};", "").replace(",", " ")
    maskdata = tuple(bitswap(int(x, 16)) for x in data.split())
    return info[:2], info[2:], cursdata, maskdata

