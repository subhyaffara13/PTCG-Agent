
def guessFileType(fileName):
    if fileName == "-":
        header = sys.stdin.buffer.peek(256)
        ext = ""
    else:
        base, ext = os.path.splitext(fileName)
        try:
            with open(fileName, "rb") as f:
                header = f.read(256)
        except IOError:
            return None

    if header.startswith(b"\xef\xbb\xbf<?xml"):
        header = header.lstrip(b"\xef\xbb\xbf")
    cr, tp = getMacCreatorAndType(fileName)
    if tp in ("sfnt", "FFIL"):
        return "TTF"
    if ext == ".dfont":
        return "TTF"
    head = Tag(header[:4])
    if head == "OTTO":
        return "OTF"
    elif head == "ttcf":
        return "TTC"
    elif head in ("\0\1\0\0", "true"):
        return "TTF"
    elif head == "wOFF":
        return "WOFF"
    elif head == "wOF2":
        return "WOFF2"
    elif head == "<?xm":
        # Use 'latin1' because that can't fail.
        header = tostr(header, "latin1")
        if opentypeheaderRE.search(header):
            return "OTX"
        else:
            return "TTX"
    return None

