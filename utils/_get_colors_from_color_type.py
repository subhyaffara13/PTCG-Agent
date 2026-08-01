
def _get_colors_from_color_type(color_type: str, num_colors: int) -> list[Color]:
    """Get colors from user input color type."""
    if color_type == "default":
        prop_cycle = mpl.rcParams["axes.prop_cycle"]
        return [
            c["color"]
            for c in itertools.islice(prop_cycle, min(num_colors, len(prop_cycle)))
        ]
    elif color_type == "random":
        return np.random.default_rng(num_colors).random((num_colors, 3)).tolist()
    else:
        raise ValueError("color_type must be either 'default' or 'random'")

