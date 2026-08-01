
def _PairPosFormat2_align_matrices(self, lst, font, transparent=False):
    matrices = [l.Class1Record for l in lst]

    # Align first classes
    self.ClassDef1, classes = _ClassDef_merge_classify(
        [l.ClassDef1 for l in lst], [l.Coverage.glyphs for l in lst]
    )
    self.Class1Count = len(classes)
    new_matrices = []
    for l, matrix in zip(lst, matrices):
        nullRow = None
        coverage = set(l.Coverage.glyphs)
        classDef1 = l.ClassDef1.classDefs
        class1Records = []
        for classSet in classes:
            exemplarGlyph = next(iter(classSet))
            if exemplarGlyph not in coverage:
                # Follow-up to e6125b353e1f54a0280ded5434b8e40d042de69f,
                # Fixes https://github.com/googlei18n/fontmake/issues/470
                # Again, revert 8d441779e5afc664960d848f62c7acdbfc71d7b9
                # when merger becomes selfless.
                nullRow = None
                if nullRow is None:
                    nullRow = ot.Class1Record()
                    class2records = nullRow.Class2Record = []
                    # TODO: When merger becomes selfless, revert e6125b353e1f54a0280ded5434b8e40d042de69f
                    for _ in range(l.Class2Count):
                        if transparent:
                            rec2 = None
                        else:
                            rec2 = ot.Class2Record()
                            rec2.Value1 = (
                                otBase.ValueRecord(self.ValueFormat1)
                                if self.ValueFormat1
                                else None
                            )
                            rec2.Value2 = (
                                otBase.ValueRecord(self.ValueFormat2)
                                if self.ValueFormat2
                                else None
                            )
                        class2records.append(rec2)
                rec1 = nullRow
            else:
                klass = classDef1.get(exemplarGlyph, 0)
                rec1 = matrix[klass]  # TODO handle out-of-range?
            class1Records.append(rec1)
        new_matrices.append(class1Records)
    matrices = new_matrices
    del new_matrices

    # Align second classes
    self.ClassDef2, classes = _ClassDef_merge_classify([l.ClassDef2 for l in lst])
    self.Class2Count = len(classes)
    new_matrices = []
    for l, matrix in zip(lst, matrices):
        classDef2 = l.ClassDef2.classDefs
        class1Records = []
        for rec1old in matrix:
            oldClass2Records = rec1old.Class2Record
            rec1new = ot.Class1Record()
            class2Records = rec1new.Class2Record = []
            for classSet in classes:
                if not classSet:  # class=0
                    rec2 = oldClass2Records[0]
                else:
                    exemplarGlyph = next(iter(classSet))
                    klass = classDef2.get(exemplarGlyph, 0)
                    rec2 = oldClass2Records[klass]
                class2Records.append(copy.deepcopy(rec2))
            class1Records.append(rec1new)
        new_matrices.append(class1Records)
    matrices = new_matrices
    del new_matrices

    return matrices

