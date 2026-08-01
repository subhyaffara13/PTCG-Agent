
def _merge_GlyphOrders(font, lst, values_lst=None, default=None):
    """Takes font and list of glyph lists (must be sorted by glyph id), and returns
    two things:
    - Combined glyph list,
    - If values_lst is None, return input glyph lists, but padded with None when a glyph
      was missing in a list.  Otherwise, return values_lst list-of-list, padded with None
      to match combined glyph lists.
    """
    if values_lst is None:
        dict_sets = [set(l) for l in lst]
    else:
        dict_sets = [{g: v for g, v in zip(l, vs)} for l, vs in zip(lst, values_lst)]
    combined = set()
    combined.update(*dict_sets)

    sortKey = font.getReverseGlyphMap().__getitem__
    order = sorted(combined, key=sortKey)
    # Make sure all input glyphsets were in proper order
    if not all(sorted(vs, key=sortKey) == vs for vs in lst):
        raise InconsistentGlyphOrder()
    del combined

    paddedValues = None
    if values_lst is None:
        padded = [
            [glyph if glyph in dict_set else default for glyph in order]
            for dict_set in dict_sets
        ]
    else:
        assert len(lst) == len(values_lst)
        padded = [
            [dict_set[glyph] if glyph in dict_set else default for glyph in order]
            for dict_set in dict_sets
        ]
    return order, padded

