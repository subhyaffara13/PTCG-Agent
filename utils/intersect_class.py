
def intersect_class(self, glyphs, klass):
    """Returns set of glyphs matching class."""
    if klass == 0:
        return set(g for g in glyphs if g not in self.classDefs)
    return set(g for g, v in self.classDefs.items() if v == klass and g in glyphs)

