
def _decode_base(value: int, dimensions: int, base: int) -> list[int]:
    digits = [0] * dimensions
    i = dimensions - 1
    while value > 0 and i >= 0:
        digits[i] = value % base
        value //= base
        i -= 1
    return digits


def _decode_base(value: int, dimensions: int, base: int) -> list[int]:
    """Decode an integer as a fixed-width vector of base-N digits (MSB first)."""
    digits = [0] * dimensions
    i = dimensions - 1
    while value > 0 and i >= 0:
        digits[i] = value % base
        value //= base
        i -= 1
    return digits

