
def measureWeight(glyphset, glyphs=None):
    """Measure the perceptual average weight of the given glyphs."""
    if isinstance(glyphs, dict):
        frequencies = glyphs
    else:
        frequencies = {g: 1 for g in glyphs}

    wght_sum = wdth_sum = 0
    for glyph_name in glyphs:
        if frequencies is not None:
            frequency = frequencies.get(glyph_name, 0)
            if frequency == 0:
                continue
        else:
            frequency = 1

        glyph = glyphset[glyph_name]

        pen = AreaPen(glyphset=glyphset)
        glyph.draw(pen)

        mult = glyph.width * frequency
        wght_sum += mult * abs(pen.value)
        wdth_sum += mult

    return wght_sum / wdth_sum

