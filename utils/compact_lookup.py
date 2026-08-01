
def compact_lookup(font: TTFont, level: int, lookup: otTables.Lookup) -> None:
    new_subtables = compact_pair_pos(font, level, lookup.SubTable)
    lookup.SubTable = new_subtables
    lookup.SubTableCount = len(new_subtables)

