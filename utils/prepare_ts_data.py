
def prepare_ts_data(
    series: Series, ax: Axes, kwargs: dict[str, Any]
) -> tuple[BaseOffset | str, Series]:
    freq, data = maybe_resample(series, ax, kwargs)

    # Set ax with freq info
    decorate_axes(ax, freq)
    # digging deeper
    if hasattr(ax, "left_ax"):
        decorate_axes(ax.left_ax, freq)
    if hasattr(ax, "right_ax"):
        decorate_axes(ax.right_ax, freq)

    return freq, data

