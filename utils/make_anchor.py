
def makeAnchor(data, klass=ot.Anchor):
    assert len(data) <= 2
    anchor = klass()
    anchor.Format = 1
    anchor.XCoordinate, anchor.YCoordinate = intSplitComma(data[0])
    if len(data) > 1 and data[1] != "":
        anchor.Format = 2
        anchor.AnchorPoint = int(data[1])
    return anchor

