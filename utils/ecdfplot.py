
def ecdfplot(
    data=None, *,
    # Vector variables
    x=None, y=None, hue=None, weights=None,
    # Computation parameters
    stat="proportion", complementary=False,
    # Hue mapping parameters
    palette=None, hue_order=None, hue_norm=None,
    # Axes information
    log_scale=None, legend=True, ax=None,
    # Other appearance keywords
    **kwargs,
):

    p = _DistributionPlotter(
        data=data,
        variables=dict(x=x, y=y, hue=hue, weights=weights),
    )

    p.map_hue(palette=palette, order=hue_order, norm=hue_norm)

    # We could support other semantics (size, style) here fairly easily
    # But it would make distplot a bit more complicated.
    # It's always possible to add features like that later, so I am going to defer.
    # It will be even easier to wait until after there is a more general/abstract
    # way to go from semantic specs to artist attributes.

    if ax is None:
        ax = plt.gca()

    p._attach(ax, log_scale=log_scale)

    color = kwargs.pop("color", kwargs.pop("c", None))
    kwargs["color"] = _default_color(ax.plot, hue, color, kwargs)

    if not p.has_xy_data:
        return ax

    # We could add this one day, but it's of dubious value
    if not p.univariate:
        raise NotImplementedError("Bivariate ECDF plots are not implemented")

    estimate_kws = dict(
        stat=stat,
        complementary=complementary,
    )

    p.plot_univariate_ecdf(
        estimate_kws=estimate_kws,
        legend=legend,
        **kwargs,
    )

    return ax

