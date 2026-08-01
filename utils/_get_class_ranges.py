
def _getClassRanges(glyphIDs: Iterable[int]):
    glyphIDs = sorted(glyphIDs)
    last = glyphIDs[0]
    ranges = [[last]]
    for glyphID in glyphIDs[1:]:
        if glyphID != last + 1:
            ranges[-1].append(last)
            ranges.append([glyphID])
        last = glyphID
    ranges[-1].append(last)
    return ranges, glyphIDs[0], glyphIDs[-1]

