
def compact_pair_pos(
    font: TTFont, level: int, subtables: Sequence[otTables.PairPos]
) -> Sequence[otTables.PairPos]:
    new_subtables = []
    for subtable in subtables:
        if subtable.Format == 1:
            # Not doing anything to Format 1 (yet?)
            new_subtables.append(subtable)
        elif subtable.Format == 2:
            new_subtables.extend(compact_class_pairs(font, level, subtable))
    return new_subtables

