
def intersect(*args, **kwargs):
    return IntersectNode(*args, **kwargs)


def intersect(self, glyphs):
    """Returns ascending list of matching coverage values."""
    return [i for i, g in enumerate(self.glyphs) if g in glyphs]


def intersect(self, glyphs):
    """Returns ascending list of matching class values."""
    return _uniq_sort(
        ([0] if any(g not in self.classDefs for g in glyphs) else [])
        + [v for g, v in self.classDefs.items() if g in glyphs]
    )

