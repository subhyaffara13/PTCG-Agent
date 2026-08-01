
def _MarkBasePosFormat1_merge(self, lst, merger, Mark="Mark", Base="Base"):
    self.ClassCount = max(l.ClassCount for l in lst)

    MarkCoverageGlyphs, MarkRecords = _merge_GlyphOrders(
        merger.font,
        [getattr(l, Mark + "Coverage").glyphs for l in lst],
        [getattr(l, Mark + "Array").MarkRecord for l in lst],
    )
    getattr(self, Mark + "Coverage").glyphs = MarkCoverageGlyphs

    BaseCoverageGlyphs, BaseRecords = _merge_GlyphOrders(
        merger.font,
        [getattr(l, Base + "Coverage").glyphs for l in lst],
        [getattr(getattr(l, Base + "Array"), Base + "Record") for l in lst],
    )
    getattr(self, Base + "Coverage").glyphs = BaseCoverageGlyphs

    # MarkArray
    records = []
    for g, glyphRecords in zip(MarkCoverageGlyphs, zip(*MarkRecords)):
        allClasses = [r.Class for r in glyphRecords if r is not None]

        # TODO Right now we require that all marks have same class in
        # all masters that cover them.  This is not required.
        #
        # We can relax that by just requiring that all marks that have
        # the same class in a master, have the same class in every other
        # master.  Indeed, if, say, a sparse master only covers one mark,
        # that mark probably will get class 0, which would possibly be
        # different from its class in other masters.
        #
        # We can even go further and reclassify marks to support any
        # input.  But, since, it's unlikely that two marks being both,
        # say, "top" in one master, and one being "top" and other being
        # "top-right" in another master, we shouldn't do that, as any
        # failures in that case will probably signify mistakes in the
        # input masters.

        if not allEqual(allClasses):
            raise ShouldBeConstant(merger, expected=allClasses[0], got=allClasses)
        else:
            rec = ot.MarkRecord()
            rec.Class = allClasses[0]
            allAnchors = [None if r is None else r.MarkAnchor for r in glyphRecords]
            if allNone(allAnchors):
                anchor = None
            else:
                anchor = ot.Anchor()
                anchor.Format = 1
                merger.mergeThings(anchor, allAnchors)
            rec.MarkAnchor = anchor
        records.append(rec)
    array = ot.MarkArray()
    array.MarkRecord = records
    array.MarkCount = len(records)
    setattr(self, Mark + "Array", array)

    # BaseArray
    records = []
    for g, glyphRecords in zip(BaseCoverageGlyphs, zip(*BaseRecords)):
        if allNone(glyphRecords):
            rec = None
        else:
            rec = getattr(ot, Base + "Record")()
            anchors = []
            setattr(rec, Base + "Anchor", anchors)
            glyphAnchors = [
                [] if r is None else getattr(r, Base + "Anchor") for r in glyphRecords
            ]
            for l in glyphAnchors:
                l.extend([None] * (self.ClassCount - len(l)))
            for allAnchors in zip(*glyphAnchors):
                if allNone(allAnchors):
                    anchor = None
                else:
                    anchor = ot.Anchor()
                    anchor.Format = 1
                    merger.mergeThings(anchor, allAnchors)
                anchors.append(anchor)
        records.append(rec)
    array = getattr(ot, Base + "Array")()
    setattr(array, Base + "Record", records)
    setattr(array, Base + "Count", len(records))
    setattr(self, Base + "Array", array)

