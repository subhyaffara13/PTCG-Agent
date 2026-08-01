
def _copy_buf(buf: list[list[Color | None]]) -> list[list[Color | None]]:
    return [row[:] for row in buf]

