
def hilite(s, color=None, bold=False):  # pragma: no cover
    """Return an highlighted version of 'string'."""
    if not term_supports_colors():
        return s
    attr = []
    colors = dict(
        blue='34',
        brown='33',
        darkgrey='30',
        green='32',
        grey='37',
        lightblue='36',
        red='91',
        violet='35',
        yellow='93',
    )
    colors[None] = '29'
    try:
        color = colors[color]
    except KeyError:
        msg = f"invalid color {color!r}; choose amongst {list(colors.keys())}"
        raise ValueError(msg) from None
    attr.append(color)
    if bold:
        attr.append('1')
    return f"\x1b[{';'.join(attr)}m{s}\x1b[0m"

