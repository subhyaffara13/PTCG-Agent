
def _round_up_to_multiple(x: int, multiple: int) -> int:
    return (x + multiple - 1) // multiple * multiple

