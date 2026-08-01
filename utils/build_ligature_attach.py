
def buildLigatureAttach(components):
    # [[Anchor, Anchor], [Anchor, Anchor, Anchor]] --> LigatureAttach
    self = ot.LigatureAttach()
    self.ComponentRecord = [buildComponentRecord(c) for c in components]
    self.ComponentCount = len(self.ComponentRecord)
    return self

