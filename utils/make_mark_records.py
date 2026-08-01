
def makeMarkRecords(data, coverage, c):
    records = []
    for glyph in coverage.glyphs:
        klass, anchor = data[glyph]
        record = c.MarkRecordClass()
        record.Class = klass
        setattr(record, c.MarkAnchor, anchor)
        records.append(record)
    return records

