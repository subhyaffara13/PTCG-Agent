
def _add_CFF2(varFont, model, master_fonts):
    from .cff import merge_region_fonts

    glyphOrder = varFont.getGlyphOrder()
    if "CFF2" not in varFont:
        from fontTools.cffLib.CFFToCFF2 import convertCFFToCFF2

        convertCFFToCFF2(varFont)

    ordered_fonts_list = model.reorderMasters(master_fonts, model.reverseMapping)
    # re-ordering the master list simplifies building the CFF2 data item lists.
    merge_region_fonts(varFont, model, ordered_fonts_list, glyphOrder)

