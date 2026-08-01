
def buildLigGlyph(coords, points):
    # ([500], [4]) --> otTables.LigGlyph; None for empty coords/points
    carets = []
    if coords:
        coords = sorted(coords, key=lambda c: c[0] if isinstance(c, tuple) else c)
        carets.extend([buildCaretValueForCoord(c) for c in coords])
    if points:
        carets.extend([buildCaretValueForPoint(p) for p in sorted(points)])
    if not carets:
        return None
    self = ot.LigGlyph()
    self.CaretValue = carets
    self.CaretCount = len(self.CaretValue)
    return self

