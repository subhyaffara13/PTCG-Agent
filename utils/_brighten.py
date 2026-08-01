
def _brighten(color: Color, amount: int) -> Color:
    return (min(255, color[0] + amount), min(255, color[1] + amount), min(255, color[2] + amount))

