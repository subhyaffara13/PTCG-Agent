import copy

def _Lookup_SinglePos_subtables_flatten(lst, font, min_inclusive_rec_format):
    glyphs, _ = _merge_GlyphOrders(font, [v.Coverage.glyphs for v in lst], None)
    num_glyphs = len(glyphs)
    new = ot.SinglePos()
    new.Format = 2
    new.ValueFormat = min_inclusive_rec_format
    new.Coverage = ot.Coverage()
    new.Coverage.glyphs = glyphs
    new.ValueCount = num_glyphs
    new.Value = [None] * num_glyphs
    for singlePos in lst:
        if singlePos.Format == 1:
            val_rec = singlePos.Value
            for gname in singlePos.Coverage.glyphs:
                i = glyphs.index(gname)
                new.Value[i] = copy.deepcopy(val_rec)
        elif singlePos.Format == 2:
            for j, gname in enumerate(singlePos.Coverage.glyphs):
                val_rec = singlePos.Value[j]
                i = glyphs.index(gname)
                new.Value[i] = copy.deepcopy(val_rec)
    return [new]

