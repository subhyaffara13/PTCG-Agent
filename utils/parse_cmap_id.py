
def parseCmapId(lines, field):
    line = next(lines)
    assert field == line[0]
    return int(line[1])

