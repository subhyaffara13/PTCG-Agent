
def VARC_remap_varidxes(self, varidxes_map):
    for glyph in self.VarCompositeGlyphs.VarCompositeGlyph:
        for component in glyph.components:
            component.axisValuesVarIndex = varidxes_map[component.axisValuesVarIndex]
            component.transformVarIndex = varidxes_map[component.transformVarIndex]

