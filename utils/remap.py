
def remap(self, coverage_map):
    """Remaps coverage."""
    self.glyphs = [self.glyphs[i] for i in coverage_map]


def remap(self, class_map):
    """Remaps classes."""
    self.classDefs = {g: class_map.index(v) for g, v in self.classDefs.items()}

