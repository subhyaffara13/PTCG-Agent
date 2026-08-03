from typing import List, Tuple

def _classDef_bytes(
    class_data: List[Tuple[List[Tuple[int, int]], int, int]],
    class_ids: List[int],
    coverage=False,
):
    if not class_ids:
        return 0
    first_ranges, min_glyph_id, max_glyph_id = class_data[class_ids[0]]
    range_count = len(first_ranges)
    for i in class_ids[1:]:
        data = class_data[i]
        range_count += len(data[0])
        min_glyph_id = min(min_glyph_id, data[1])
        max_glyph_id = max(max_glyph_id, data[2])
    glyphCount = max_glyph_id - min_glyph_id + 1
    # https://docs.microsoft.com/en-us/typography/opentype/spec/chapter2#class-definition-table-format-1
    format1_bytes = 6 + glyphCount * 2
    # https://docs.microsoft.com/en-us/typography/opentype/spec/chapter2#class-definition-table-format-2
    format2_bytes = 4 + range_count * 6
    return min(format1_bytes, format2_bytes)

