
def _ClassDef_invert(self, allGlyphs=None):
    if isinstance(self, dict):
        classDefs = self
    else:
        classDefs = self.classDefs if self and self.classDefs else {}
    m = max(classDefs.values()) if classDefs else 0

    ret = []
    for _ in range(m + 1):
        ret.append(set())

    for k, v in classDefs.items():
        ret[v].add(k)

    # Class-0 is special.  It's "everything else".
    if allGlyphs is None:
        ret[0] = None
    else:
        # Limit all classes to glyphs in allGlyphs.
        # Collect anything without a non-zero class into class=zero.
        ret[0] = class0 = set(allGlyphs)
        for s in ret[1:]:
            s.intersection_update(class0)
            class0.difference_update(s)

    return ret

