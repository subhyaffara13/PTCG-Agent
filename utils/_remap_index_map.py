
def _remap_index_map(s, varidx_map, table_map):
    map_ = {k: varidx_map[v] for k, v in table_map.mapping.items()}
    # Emptied glyphs are remapped to:
    # if GID <= last retained GID, 0/0: delta set for 0/0 is expected to exist & zeros compress well
    # if GID > last retained GID, major/minor of the last retained glyph: will be optimized out by table compiler
    last_idx = varidx_map[table_map.mapping[s.last_retained_glyph]]
    for g, i in s.reverseEmptiedGlyphMap.items():
        map_[g] = last_idx if i > s.last_retained_order else 0
    return map_

