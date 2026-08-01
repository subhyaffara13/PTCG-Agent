
def subset(self, glyphs):
    """Returns ascending list of remaining coverage values."""
    indices = self.intersect(glyphs)
    self.glyphs = [g for g in self.glyphs if g in glyphs]
    return indices


def subset(self, glyphs, remap=False, useClass0=True):
    """Returns ascending list of remaining classes."""
    self.classDefs = {g: v for g, v in self.classDefs.items() if g in glyphs}
    # Note: while class 0 has the special meaning of "not matched",
    # if no glyph will ever /not match/, we can optimize class 0 out too.
    # Only do this if allowed.
    indices = _uniq_sort(
        (
            [0]
            if ((not useClass0) or any(g not in self.classDefs for g in glyphs))
            else []
        )
        + list(self.classDefs.values())
    )
    if remap:
        self.remap(indices)
    return indices

