
def parseMarkFilteringSets(lines, font):
    sets = {}
    with lines.between("set definition"):
        for line in lines:
            assert len(line) == 2, line
            glyph = makeGlyph(line[0])
            # TODO accept set names
            st = int(line[1])
            if st not in sets:
                sets[st] = []
            sets[st].append(glyph)
    return makeMarkFilteringSets(sets, font)

