
def scatterplot(
    data=None, *,
    x=None, y=None, hue=None, size=None, style=None,
    palette=None, hue_order=None, hue_norm=None,
    sizes=None, size_order=None, size_norm=None,
    markers=True, style_order=None, legend="auto", ax=None,
    **kwargs
):

    p = _ScatterPlotter(
        data=data,
        variables=dict(x=x, y=y, hue=hue, size=size, style=style),
        legend=legend
    )

    p.map_hue(palette=palette, order=hue_order, norm=hue_norm)
    p.map_size(sizes=sizes, order=size_order, norm=size_norm)
    p.map_style(markers=markers, order=style_order)

    if ax is None:
        ax = plt.gca()

    if not p.has_xy_data:
        return ax

    p._attach(ax)

    color = kwargs.pop("color", None)
    kwargs["color"] = _default_color(ax.scatter, hue, color, kwargs)

    p.plot(ax, kwargs)

    return ax

