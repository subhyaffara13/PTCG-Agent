
def intersect_glyphs(self, glyphs):
    """Returns set of intersecting glyphs."""
    return set(g for g in self.glyphs if g in glyphs)

