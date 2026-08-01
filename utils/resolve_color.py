
def resolve_color(
    mark: Mark,
    data: DataFrame | dict,
    prefix: str = "",
    scales: dict[str, Scale] | None = None,
) -> RGBATuple | ndarray:
    """
    Obtain a default, specified, or mapped value for a color feature.

    This method exists separately to support the relationship between a
    color and its corresponding alpha. We want to respect alpha values that
    are passed in specified (or mapped) color values but also make use of a
    separate `alpha` variable, which can be mapped. This approach may also
    be extended to support mapping of specific color channels (i.e.
    luminance, chroma) in the future.

    Parameters
    ----------
    mark :
        Mark with the color property.
    data :
        Container with data values for features that will be semantically mapped.
    prefix :
        Support "color", "fillcolor", etc.

    """
    color = mark._resolve(data, f"{prefix}color", scales)

    if f"{prefix}alpha" in mark._mappable_props:
        alpha = mark._resolve(data, f"{prefix}alpha", scales)
    else:
        alpha = mark._resolve(data, "alpha", scales)

    def visible(x, axis=None):
        """Detect "invisible" colors to set alpha appropriately."""
        # TODO First clause only needed to handle non-rgba arrays,
        # which we are trying to handle upstream
        return np.array(x).dtype.kind != "f" or np.isfinite(x).all(axis)

    # Second check here catches vectors of strings with identity scale
    # It could probably be handled better upstream. This is a tricky problem
    if np.ndim(color) < 2 and all(isinstance(x, float) for x in color):
        if len(color) == 4:
            return mpl.colors.to_rgba(color)
        alpha = alpha if visible(color) else np.nan
        return mpl.colors.to_rgba(color, alpha)
    else:
        if np.ndim(color) == 2 and color.shape[1] == 4:
            return mpl.colors.to_rgba_array(color)
        alpha = np.where(visible(color, axis=1), alpha, np.nan)
        return mpl.colors.to_rgba_array(color, alpha)

