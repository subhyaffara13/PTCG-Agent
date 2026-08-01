
def bdf_char(
    f: BinaryIO,
) -> (
    tuple[
        str,
        int,
        tuple[tuple[int, int], tuple[int, int, int, int], tuple[int, int, int, int]],
        Image.Image,
    ]
    | None
):
    # skip to STARTCHAR
    while True:
        s = f.readline()
        if not s:
            return None
        if s.startswith(b"STARTCHAR"):
            break
    id = s[9:].strip().decode("ascii")

    # load symbol properties
    props = {}
    while True:
        s = f.readline()
        if not s or s.startswith(b"BITMAP"):
            break
        i = s.find(b" ")
        props[s[:i].decode("ascii")] = s[i + 1 : -1].decode("ascii")

    # load bitmap
    bitmap = bytearray()
    while True:
        s = f.readline()
        if not s or s.startswith(b"ENDCHAR"):
            break
        bitmap += s[:-1]

    # The word BBX
    # followed by the width in x (BBw), height in y (BBh),
    # and x and y displacement (BBxoff0, BByoff0)
    # of the lower left corner from the origin of the character.
    width, height, x_disp, y_disp = (int(p) for p in props["BBX"].split())
    Image._decompression_bomb_check((width, height))

    # The word DWIDTH
    # followed by the width in x and y of the character in device pixels.
    dwx, dwy = (int(p) for p in props["DWIDTH"].split())

    bbox = (
        (dwx, dwy),
        (x_disp, -y_disp - height, width + x_disp, -y_disp),
        (0, 0, width, height),
    )

    try:
        im = Image.frombytes("1", (width, height), bitmap, "hex", "1")
    except ValueError:
        # deal with zero-width characters
        im = Image.new("1", (width, height))

    return id, int(props["ENCODING"]), bbox, im

