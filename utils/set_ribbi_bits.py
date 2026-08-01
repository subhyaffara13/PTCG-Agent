
def setRibbiBits(font):
    """Set the `head.macStyle` and `OS/2.fsSelection` style bits
    appropriately."""

    english_ribbi_style = font["name"].getName(names.NameID.SUBFAMILY_NAME, 3, 1, 0x409)
    if english_ribbi_style is None:
        return

    styleMapStyleName = english_ribbi_style.toStr().lower()
    if styleMapStyleName not in {"regular", "bold", "italic", "bold italic"}:
        return

    if styleMapStyleName == "bold":
        font["head"].macStyle = 0b01
    elif styleMapStyleName == "bold italic":
        font["head"].macStyle = 0b11
    elif styleMapStyleName == "italic":
        font["head"].macStyle = 0b10

    selection = font["OS/2"].fsSelection
    # First clear...
    selection &= ~(1 << 0)
    selection &= ~(1 << 5)
    selection &= ~(1 << 6)
    # ...then re-set the bits.
    if styleMapStyleName == "regular":
        selection |= 1 << 6
    elif styleMapStyleName == "bold":
        selection |= 1 << 5
    elif styleMapStyleName == "italic":
        selection |= 1 << 0
    elif styleMapStyleName == "bold italic":
        selection |= 1 << 0
        selection |= 1 << 5
    font["OS/2"].fsSelection = selection

