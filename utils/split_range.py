
def splitRange(startCode, endCode, cmap):
    # Try to split a range of character codes into subranges with consecutive
    # glyph IDs in such a way that the cmap4 subtable can be stored "most"
    # efficiently. I can't prove I've got the optimal solution, but it seems
    # to do well with the fonts I tested: none became bigger, many became smaller.
    if startCode == endCode:
        return [], [endCode]

    lastID = cmap[startCode]
    lastCode = startCode
    inOrder = None
    orderedBegin = None
    subRanges = []

    # Gather subranges in which the glyph IDs are consecutive.
    for code in range(startCode + 1, endCode + 1):
        glyphID = cmap[code]

        if glyphID - 1 == lastID:
            if inOrder is None or not inOrder:
                inOrder = 1
                orderedBegin = lastCode
        else:
            if inOrder:
                inOrder = 0
                subRanges.append((orderedBegin, lastCode))
                orderedBegin = None

        lastID = glyphID
        lastCode = code

    if inOrder:
        subRanges.append((orderedBegin, lastCode))
    assert lastCode == endCode

    # Now filter out those new subranges that would only make the data bigger.
    # A new segment cost 8 bytes, not using a new segment costs 2 bytes per
    # character.
    newRanges = []
    for b, e in subRanges:
        if b == startCode and e == endCode:
            break  # the whole range, we're fine
        if b == startCode or e == endCode:
            threshold = 4  # split costs one more segment
        else:
            threshold = 8  # split costs two more segments
        if (e - b + 1) > threshold:
            newRanges.append((b, e))
    subRanges = newRanges

    if not subRanges:
        return [], [endCode]

    if subRanges[0][0] != startCode:
        subRanges.insert(0, (startCode, subRanges[0][0] - 1))
    if subRanges[-1][1] != endCode:
        subRanges.append((subRanges[-1][1] + 1, endCode))

    # Fill the "holes" in the segments list -- those are the segments in which
    # the glyph IDs are _not_ consecutive.
    i = 1
    while i < len(subRanges):
        if subRanges[i - 1][1] + 1 != subRanges[i][0]:
            subRanges.insert(i, (subRanges[i - 1][1] + 1, subRanges[i][0] - 1))
            i = i + 1
        i = i + 1

    # Transform the ranges into startCode/endCode lists.
    start = []
    end = []
    for b, e in subRanges:
        start.append(b)
        end.append(e)
    start.pop(0)

    assert len(start) + 1 == len(end)
    return start, end

