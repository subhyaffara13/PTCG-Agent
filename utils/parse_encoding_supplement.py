
def parseEncodingSupplement(file, encoding, strings):
    """
    Parse the CFF Encoding supplement data:
      - nSups: number of supplementary mappings
      - each mapping: (code, SID) pair
    and apply them to the `encoding` list in place.
    """
    nSups = readCard8(file)
    for _ in range(nSups):
        code = readCard8(file)
        sid = readSID(file)
        name = strings[sid]
        encoding[code] = name

