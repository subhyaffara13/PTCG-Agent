
def _ClassDef_merge_classify(lst, allGlyphses=None):
    self = ot.ClassDef()
    self.classDefs = classDefs = {}
    allGlyphsesWasNone = allGlyphses is None
    if allGlyphsesWasNone:
        allGlyphses = [None] * len(lst)

    classifier = classifyTools.Classifier()
    for classDef, allGlyphs in zip(lst, allGlyphses):
        sets = _ClassDef_invert(classDef, allGlyphs)
        if allGlyphs is None:
            sets = sets[1:]
        classifier.update(sets)
    classes = classifier.getClasses()

    if allGlyphsesWasNone:
        classes.insert(0, set())

    for i, classSet in enumerate(classes):
        if i == 0:
            continue
        for g in classSet:
            classDefs[g] = i

    return self, classes

