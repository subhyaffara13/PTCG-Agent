
def _bar(current: float, total: float, width: int = _BAR_WIDTH) -> str:
    if total <= 0:
        return "░" * width
    filled = int(min(current / total, 1.0) * width)
    return "█" * filled + "░" * (width - filled)


def _bar(
    data: NDFrame,
    align: str | float | Callable,
    colors: str | list | tuple,
    cmap: Any,
    width: float,
    height: float,
    vmin: float | None,
    vmax: float | None,
    base_css: str,
):
    """
    Draw bar chart in data cells using HTML CSS linear gradient.

    Parameters
    ----------
    data : Series or DataFrame
        Underling subset of Styler data on which operations are performed.
    align : str in {"left", "right", "mid", "zero", "mean"}, int, float, callable
        Method for how bars are structured or scalar value of centre point.
    colors : list-like of str
        Two listed colors as string in valid CSS.
    width : float in [0,1]
        The percentage of the cell, measured from left, where drawn bars will reside.
    height : float in [0,1]
        The percentage of the cell's height where drawn bars will reside, centrally
        aligned.
    vmin : float, optional
        Overwrite the minimum value of the window.
    vmax : float, optional
        Overwrite the maximum value of the window.
    base_css : str
        Additional CSS that is included in the cell before bars are drawn.
    """

    def css_bar(start: float, end: float, color: str) -> str:
        """
        Generate CSS code to draw a bar from start to end in a table cell.

        Uses linear-gradient.

        Parameters
        ----------
        start : float
            Relative positional start of bar coloring in [0,1]
        end : float
            Relative positional end of the bar coloring in [0,1]
        color : str
            CSS valid color to apply.

        Returns
        -------
        str : The CSS applicable to the cell.

        Notes
        -----
        Uses ``base_css`` from outer scope.
        """
        cell_css = base_css
        if end > start:
            cell_css += "background: linear-gradient(90deg,"
            if start > 0:
                cell_css += (
                    f" transparent {start * 100:.1f}%, {color} {start * 100:.1f}%,"
                )
            cell_css += f" {color} {end * 100:.1f}%, transparent {end * 100:.1f}%)"
        return cell_css

    def css_calc(x, left: float, right: float, align: str, color: str | list | tuple):
        """
        Return the correct CSS for bar placement based on calculated values.

        Parameters
        ----------
        x : float
            Value which determines the bar placement.
        left : float
            Value marking the left side of calculation, usually minimum of data.
        right : float
            Value marking the right side of the calculation, usually maximum of data
            (left < right).
        align : {"left", "right", "zero", "mid"}
            How the bars will be positioned.
            "left", "right", "zero" can be used with any values for ``left``, ``right``.
            "mid" can only be used where ``left <= 0`` and ``right >= 0``.
            "zero" is used to specify a center when all values ``x``, ``left``,
            ``right`` are translated, e.g. by say a mean or median.

        Returns
        -------
        str : Resultant CSS with linear gradient.

        Notes
        -----
        Uses ``colors``, ``width`` and ``height`` from outer scope.
        """
        if pd.isna(x):
            return base_css

        if isinstance(color, (list, tuple)):
            color = color[0] if x < 0 else color[1]
        assert isinstance(color, str)  # mypy redefinition

        x = left if x < left else x
        x = right if x > right else x  # trim data if outside of the window

        start: float = 0
        end: float = 1

        if align == "left":
            # all proportions are measured from the left side between left and right
            end = (x - left) / (right - left)

        elif align == "right":
            # all proportions are measured from the right side between left and right
            start = (x - left) / (right - left)

        else:
            z_frac: float = 0.5  # location of zero based on the left-right range
            if align == "zero":
                # all proportions are measured from the center at zero
                limit: float = max(abs(left), abs(right))
                left, right = -limit, limit
            elif align == "mid":
                # bars drawn from zero either leftwards or rightwards with center at mid
                mid: float = (left + right) / 2
                z_frac = (
                    -mid / (right - left) + 0.5 if mid < 0 else -left / (right - left)
                )

            if x < 0:
                start, end = (x - left) / (right - left), z_frac
            else:
                start, end = z_frac, (x - left) / (right - left)

        ret = css_bar(start * width, end * width, color)
        if height < 1 and "background: linear-gradient(" in ret:
            return (
                ret + f" no-repeat center; background-size: 100% {height * 100:.1f}%;"
            )
        else:
            return ret

    values = data.to_numpy()
    # A tricky way to address the issue where np.nanmin/np.nanmax fail to handle pd.NA.
    left = np.nanmin(data.min(skipna=True)) if vmin is None else vmin
    right = np.nanmax(data.max(skipna=True)) if vmax is None else vmax
    z: float = 0  # adjustment to translate data

    if align == "mid":
        if left >= 0:  # "mid" is documented to act as "left" if all values positive
            align, left = "left", 0 if vmin is None else vmin
        elif right <= 0:  # "mid" is documented to act as "right" if all values negative
            align, right = "right", 0 if vmax is None else vmax
    elif align == "mean":
        z, align = np.nanmean(values), "zero"
    elif callable(align):
        z, align = align(values), "zero"
    elif isinstance(align, (float, int)):
        z, align = float(align), "zero"
    elif align not in ("left", "right", "zero"):
        raise ValueError(
            "`align` should be in {'left', 'right', 'mid', 'mean', 'zero'} or be a "
            "value defining the center line or a callable that returns a float"
        )

    rgbas = None
    if cmap is not None:
        # use the matplotlib colormap input
        _matplotlib = import_optional_dependency(
            "matplotlib", extra="Styler.bar requires matplotlib."
        )
        cmap = (
            _matplotlib.colormaps[cmap]
            if isinstance(cmap, str)
            else cmap  # assumed to be a Colormap instance as documented
        )
        norm = _matplotlib.colors.Normalize(left, right)
        rgbas = cmap(norm(values))
        if data.ndim == 1:
            rgbas = [_matplotlib.colors.rgb2hex(rgba) for rgba in rgbas]
        else:
            rgbas = [
                [_matplotlib.colors.rgb2hex(rgba) for rgba in row] for row in rgbas
            ]

    assert isinstance(align, str)  # mypy: should now be in [left, right, mid, zero]
    if data.ndim == 1:
        return [
            css_calc(
                x - z, left - z, right - z, align, colors if rgbas is None else rgbas[i]
            )
            for i, x in enumerate(values)
        ]
    else:
        return np.array(
            [
                [
                    css_calc(
                        x - z,
                        left - z,
                        right - z,
                        align,
                        colors if rgbas is None else rgbas[i][j],
                    )
                    for j, x in enumerate(row)
                ]
                for i, row in enumerate(values)
            ]
        )

