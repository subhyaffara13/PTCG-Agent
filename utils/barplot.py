
def barplot(
    data=None, *, x=None, y=None, hue=None, order=None, hue_order=None,
    estimator="mean", errorbar=("ci", 95), n_boot=1000, seed=None, units=None,
    weights=None, orient=None, color=None, palette=None, saturation=.75,
    fill=True, hue_norm=None, width=.8, dodge="auto", gap=0, log_scale=None,
    native_scale=False, formatter=None, legend="auto", capsize=0, err_kws=None,
    ci=deprecated, errcolor=deprecated, errwidth=deprecated, ax=None, **kwargs,
):

    errorbar = utils._deprecate_ci(errorbar, ci)

    # Be backwards compatible with len passed directly, which
    # does not work in Series.agg (maybe a pandas bug?)
    if estimator is len:
        estimator = "size"

    p = _CategoricalAggPlotter(
        data=data,
        variables=dict(x=x, y=y, hue=hue, units=units, weight=weights),
        order=order,
        orient=orient,
        color=color,
        legend=legend,
    )

    if ax is None:
        ax = plt.gca()

    if p.plot_data.empty:
        return ax

    if dodge == "auto":
        # Needs to be before scale_categorical changes the coordinate series dtype
        dodge = p._dodge_needed()

    if p.var_types.get(p.orient) == "categorical" or not native_scale:
        p.scale_categorical(p.orient, order=order, formatter=formatter)

    p._attach(ax, log_scale=log_scale)

    # Deprecations to remove in v0.14.0.
    hue_order = p._palette_without_hue_backcompat(palette, hue_order)
    palette, hue_order = p._hue_backcompat(color, palette, hue_order)

    saturation = saturation if fill else 1
    p.map_hue(palette=palette, order=hue_order, norm=hue_norm, saturation=saturation)
    color = _default_color(ax.bar, hue, color, kwargs, saturation=saturation)

    agg_cls = WeightedAggregator if "weight" in p.plot_data else EstimateAggregator
    aggregator = agg_cls(estimator, errorbar, n_boot=n_boot, seed=seed)
    err_kws = {} if err_kws is None else normalize_kwargs(err_kws, mpl.lines.Line2D)

    # Deprecations to remove in v0.15.0.
    err_kws, capsize = p._err_kws_backcompat(err_kws, errcolor, errwidth, capsize)

    p.plot_bars(
        aggregator=aggregator,
        dodge=dodge,
        width=width,
        gap=gap,
        color=color,
        fill=fill,
        capsize=capsize,
        err_kws=err_kws,
        plot_kws=kwargs,
    )

    p._add_axis_labels(ax)
    p._adjust_cat_axis(ax, axis=p.orient)

    return ax

