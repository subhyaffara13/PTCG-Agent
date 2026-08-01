
def compact_ext_lookup(font: TTFont, level: int, lookup: otTables.Lookup) -> None:
    new_subtables = compact_pair_pos(
        font, level, [ext_subtable.ExtSubTable for ext_subtable in lookup.SubTable]
    )
    new_ext_subtables = []
    for subtable in new_subtables:
        ext_subtable = otTables.ExtensionPos()
        ext_subtable.Format = 1
        ext_subtable.ExtSubTable = subtable
        new_ext_subtables.append(ext_subtable)
    lookup.SubTable = new_ext_subtables
    lookup.SubTableCount = len(new_ext_subtables)

