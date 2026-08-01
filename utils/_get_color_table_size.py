
def _get_color_table_size(palette_bytes: bytes) -> int:
    # calculate the palette size for the header
    if not palette_bytes:
        return 0
    elif len(palette_bytes) < 9:
        return 1
    else:
        return math.ceil(math.log(len(palette_bytes) // 3, 2)) - 1

