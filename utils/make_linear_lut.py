
def make_linear_lut(black: int, white: float) -> list[int]:
    if black == 0:
        return [int(white * i // 255) for i in range(256)]

    msg = "unavailable when black is non-zero"
    raise NotImplementedError(msg)  # FIXME

