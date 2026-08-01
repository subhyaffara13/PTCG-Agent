
def from_levels_and_colors(levels, colors, extend='neither'):
    """
    A helper routine to generate a cmap and a norm instance which
    behave similar to contourf's levels and colors arguments.

    Parameters
    ----------
    levels : sequence of numbers
        The quantization levels used to construct the `BoundaryNorm`.
        Value ``v`` is quantized to level ``i`` if ``lev[i] <= v < lev[i+1]``.
    colors : sequence of colors
        The fill color to use for each level. If *extend* is "neither" there
        must be ``n_level - 1`` colors. For an *extend* of "min" or "max" add
        one extra color, and for an *extend* of "both" add two colors.
    extend : {'neither', 'min', 'max', 'both'}, optional
        The behaviour when a value falls out of range of the given levels.
        See `~.Axes.contourf` for details.

    Returns
    -------
    cmap : `~matplotlib.colors.Colormap`
    norm : `~matplotlib.colors.Normalize`
    """
    slice_map = {
        'both': slice(1, -1),
        'min': slice(1, None),
        'max': slice(0, -1),
        'neither': slice(0, None),
    }
    _api.check_in_list(slice_map, extend=extend)
    color_slice = slice_map[extend]

    n_data_colors = len(levels) - 1
    n_extend_colors = color_slice.start - (color_slice.stop or 0)  # 0, 1 or 2
    n_expected = n_data_colors + n_extend_colors
    if len(colors) != n_expected:
        raise ValueError(
            f'Expected {n_expected} colors ({n_data_colors} colors for {len(levels)} '
            f'levels, and {n_extend_colors} colors for extend == {extend!r}), '
            f'but got {len(colors)}')

    data_colors = colors[color_slice]
    under_color = colors[0] if extend in ['min', 'both'] else 'none'
    over_color = colors[-1] if extend in ['max', 'both'] else 'none'
    cmap = ListedColormap(data_colors, under=under_color, over=over_color)

    cmap.colorbar_extend = extend

    norm = BoundaryNorm(levels, ncolors=n_data_colors)
    return cmap, norm

