
def vertical_grid_grouped(**interface: Any) -> str:
    return (
        _vertical_grid_common(need_trailing_char=False, **interface)
        + str(interface["line_separator"])
        + ")"
    )

