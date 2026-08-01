
def pointplot(
    data=None, *, x=None, y=None, hue=None, order=None, hue_order=None,
    estimator="mean", errorbar=("ci", 95), n_boot=1000, seed=None, units=None,
    weights=None, color=None, palette=None, hue_norm=None, markers=default,
    linestyles=default, dodge=False, log_scale=None, native_scale=False,
    orient=None, capsize=0, formatter=None, legend="auto", err_kws=None,
    ci=deprecated, errwidth=deprecated, join=deprecated, scale=deprecated,
    ax=None, **kwargs,
):

    errorbar = utils._deprecate_ci(errorbar, ci)

    p = _CategoricalAggPlotter(
        data=data,
        variables=dict(x=x, y=y, hue=hue, units=units, weight=weights),
        order=order,
        orient=orient,
        # Handle special backwards compatibility where pointplot originally
        # did *not* default to multi-colored unless a palette was specified.
        color="C0" if (color is None and palette is None) else color,
        legend=legend,
    )

    if ax is None:
        ax = plt.gca()

    if p.plot_data.empty:
        return ax

    if p.var_types.get(p.orient) == "categorical" or not native_scale:
        p.scale_categorical(p.orient, order=order, formatter=formatter)

    p._attach(ax, log_scale=log_scale)

    # Deprecations to remove in v0.14.0.
    hue_order = p._palette_without_hue_backcompat(palette, hue_order)
    palette, hue_order = p._hue_backcompat(color, palette, hue_order)

    p.map_hue(palette=palette, order=hue_order, norm=hue_norm)
    color = _default_color(ax.plot, hue, color, kwargs)

    agg_cls = WeightedAggregator if "weight" in p.plot_data else EstimateAggregator
    aggregator = agg_cls(estimator, errorbar, n_boot=n_boot, seed=seed)
    err_kws = {} if err_kws is None else normalize_kwargs(err_kws, mpl.lines.Line2D)

    # Deprecations to remove in v0.15.0.
    p._point_kwargs_backcompat(scale, join, kwargs)
    err_kws, capsize = p._err_kws_backcompat(err_kws, None, errwidth, capsize)

    p.plot_points(
        aggregator=aggregator,
        markers=markers,
        linestyles=linestyles,
        dodge=dodge,
        color=color,
        capsize=capsize,
        err_kws=err_kws,
        plot_kws=kwargs,
    )

    p._add_axis_labels(ax)
    p._adjust_cat_axis(ax, axis=p.orient)

    return ax

