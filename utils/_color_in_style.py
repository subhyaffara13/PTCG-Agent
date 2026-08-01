
def _color_in_style(style: str) -> bool:
    """
    Check if there is a color letter in the style string.
    """
    return not set(mpl.colors.BASE_COLORS).isdisjoint(style)

