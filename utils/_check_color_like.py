
def _check_color_like(**kwargs):
    """
    For each *key, value* pair in *kwargs*, check that *value* is color-like.
    """
    for k, v in kwargs.items():
        if not is_color_like(v):
            raise ValueError(
                f"{v!r} is not a valid value for {k}: supported inputs are "
                f"(r, g, b) and (r, g, b, a) 0-1 float tuples; "
                f"'#rrggbb', '#rrggbbaa', '#rgb', '#rgba' strings; "
                f"named color strings; "
                f"string reprs of 0-1 floats for grayscale values; "
                f"'C0', 'C1', ... strings for colors of the color cycle; "
                f"and pairs combining one of the above with an alpha value")

