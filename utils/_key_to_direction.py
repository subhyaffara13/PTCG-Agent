
def _key_to_direction(key: str) -> tuple[int, int]:
    match key:
        case "w" | "W" | "\x1b[A":
            return -1, 0
        case "s" | "S" | "\x1b[B":
            return 1, 0
        case "a" | "A" | "\x1b[D":
            return 0, -1
        case "d" | "D" | "\x1b[C":
            return 0, 1
        case _:
            return 0, 0

