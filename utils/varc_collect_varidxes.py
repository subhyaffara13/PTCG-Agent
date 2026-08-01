
def VARC_collect_varidxes(self, varidxes):
    for glyph in self.VarCompositeGlyphs.VarCompositeGlyph:
        for component in glyph.components:
            varidxes.add(component.axisValuesVarIndex)
            varidxes.add(component.transformVarIndex)

