
def lineplot(
    data=None, *,
    x=None, y=None, hue=None, size=None, style=None, units=None, weights=None,
    palette=None, hue_order=None, hue_norm=None,
    sizes=None, size_order=None, size_norm=None,
    dashes=True, markers=None, style_order=None,
    estimator="mean", errorbar=("ci", 95), n_boot=1000, seed=None,
    orient="x", sort=True, err_style="band", err_kws=None,
    legend="auto", ci="deprecated", ax=None, **kwargs
):

    # Handle deprecation of ci parameter
    errorbar = _deprecate_ci(errorbar, ci)

    p = _LinePlotter(
        data=data,
        variables=dict(
            x=x, y=y, hue=hue, size=size, style=style, units=units, weight=weights
        ),
        estimator=estimator, n_boot=n_boot, seed=seed, errorbar=errorbar,
        sort=sort, orient=orient, err_style=err_style, err_kws=err_kws,
        legend=legend,
    )

    p.map_hue(palette=palette, order=hue_order, norm=hue_norm)
    p.map_size(sizes=sizes, order=size_order, norm=size_norm)
    p.map_style(markers=markers, dashes=dashes, order=style_order)

    if ax is None:
        ax = plt.gca()

    if "style" not in p.variables and not {"ls", "linestyle"} & set(kwargs):  # XXX
        kwargs["dashes"] = "" if dashes is None or isinstance(dashes, bool) else dashes

    if not p.has_xy_data:
        return ax

    p._attach(ax)

    # Other functions have color as an explicit param,
    # and we should probably do that here too
    color = kwargs.pop("color", kwargs.pop("c", None))
    kwargs["color"] = _default_color(ax.plot, hue, color, kwargs)

    p.plot(ax, kwargs)
    return ax

