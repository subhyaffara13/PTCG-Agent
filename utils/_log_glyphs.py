
def _log_glyphs(self, glyphs, font=None):
    self.info("Glyph names: %s", sorted(glyphs))
    if font:
        reverseGlyphMap = font.getReverseGlyphMap()
        self.info("Glyph IDs:   %s", sorted(reverseGlyphMap[g] for g in glyphs))

