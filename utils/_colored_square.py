
def _colored_square(color: Color) -> str:
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m■\033[0m"

