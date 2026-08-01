
def buildBaseRecord(anchors):
    # [otTables.Anchor, otTables.Anchor, ...] --> otTables.BaseRecord
    self = ot.BaseRecord()
    self.BaseAnchor = anchors
    return self

