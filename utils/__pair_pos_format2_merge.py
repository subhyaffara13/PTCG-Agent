
def _PairPosFormat2_merge(self, lst, merger):
    assert allEqual(
        [l.ValueFormat2 == 0 for l in lst if l.Class1Record]
    ), "Report bug against fonttools."

    merger.mergeObjects(
        self,
        lst,
        exclude=(
            "Coverage",
            "ClassDef1",
            "Class1Count",
            "ClassDef2",
            "Class2Count",
            "Class1Record",
            "ValueFormat1",
            "ValueFormat2",
        ),
    )

    # Align coverages
    glyphs, _ = _merge_GlyphOrders(merger.font, [v.Coverage.glyphs for v in lst])
    self.Coverage.glyphs = glyphs

    # Currently, if the coverage of PairPosFormat2 subtables are different,
    # we do NOT bother walking down the subtable list when filling in new
    # rows for alignment.  As such, this is only correct if current subtable
    # is the last subtable in the lookup.  Ensure that.
    #
    # Note that our canonicalization process merges trailing PairPosFormat2's,
    # so in reality this is rare.
    for l, subtables in zip(lst, merger.lookup_subtables):
        if l.Coverage.glyphs != glyphs:
            assert l == subtables[-1]

    matrices = _PairPosFormat2_align_matrices(self, lst, merger.font)

    self.Class1Record = list(matrices[0])  # TODO move merger to be selfless
    merger.mergeLists(self.Class1Record, matrices)

