
def makeBaseRecords(data, coverage, c, classCount):
    records = []
    idx = {}
    for glyph in coverage.glyphs:
        idx[glyph] = len(records)
        record = c.BaseRecordClass()
        anchors = [None] * classCount
        setattr(record, c.BaseAnchor, anchors)
        records.append(record)
    for (glyph, klass), anchor in data.items():
        record = records[idx[glyph]]
        anchors = getattr(record, c.BaseAnchor)
        assert anchors[klass] is None, (glyph, klass)
        anchors[klass] = anchor
    return records

