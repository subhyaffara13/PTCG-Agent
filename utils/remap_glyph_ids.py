from typing import Dict

def remap_glyph_ids(
    svg: etree.Element, glyph_index_map: Dict[int, int]
) -> Dict[str, str]:
    # Given {old_gid: new_gid} map, rename all elements containing id="glyph{gid}"
    # special attributes
    elements = group_elements_by_id(svg)
    id_map = {}
    for el_id, el in elements.items():
        m = GID_RE.match(el_id)
        if not m:
            continue
        old_index = int(m.group(1))
        new_index = glyph_index_map.get(old_index)
        if new_index is not None:
            if old_index == new_index:
                continue
            new_id = f"glyph{new_index}"
        else:
            # If the old index is missing, the element correspond to a glyph that was
            # excluded from the font's subset.
            # We rename it to avoid clashes with the new GIDs or other element ids.
            new_id = f".{el_id}"
            n = count(1)
            while new_id in elements:
                new_id = f"{new_id}.{next(n)}"

        id_map[el_id] = new_id
        el.attrib["id"] = new_id

    return id_map

