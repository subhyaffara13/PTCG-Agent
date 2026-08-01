
def buildMark2Record(anchors):
    # [otTables.Anchor, otTables.Anchor, ...] --> otTables.Mark2Record
    self = ot.Mark2Record()
    self.Mark2Anchor = anchors
    return self

