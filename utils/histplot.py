
def histplot(
    data=None, *,
    # Vector variables
    x=None, y=None, hue=None, weights=None,
    # Histogram computation parameters
    stat="count", bins="auto", binwidth=None, binrange=None,
    discrete=None, cumulative=False, common_bins=True, common_norm=True,
    # Histogram appearance parameters
    multiple="layer", element="bars", fill=True, shrink=1,
    # Histogram smoothing with a kernel density estimate
    kde=False, kde_kws=None, line_kws=None,
    # Bivariate histogram parameters
    thresh=0, pthresh=None, pmax=None, cbar=False, cbar_ax=None, cbar_kws=None,
    # Hue mapping parameters
    palette=None, hue_order=None, hue_norm=None, color=None,
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

    if ax is None:
        ax = plt.gca()

    p._attach(ax, log_scale=log_scale)

    if p.univariate:  # Note, bivariate plots won't cycle
        if fill:
            method = ax.bar if element == "bars" else ax.fill_between
        else:
            method = ax.plot
        color = _default_color(method, hue, color, kwargs)

    if not p.has_xy_data:
        return ax

    # Default to discrete bins for categorical variables
    if discrete is None:
        discrete = p._default_discrete()

    estimate_kws = dict(
        stat=stat,
        bins=bins,
        binwidth=binwidth,
        binrange=binrange,
        discrete=discrete,
        cumulative=cumulative,
    )

    if p.univariate:

        p.plot_univariate_histogram(
            multiple=multiple,
            element=element,
            fill=fill,
            shrink=shrink,
            common_norm=common_norm,
            common_bins=common_bins,
            kde=kde,
            kde_kws=kde_kws,
            color=color,
            legend=legend,
            estimate_kws=estimate_kws,
            line_kws=line_kws,
            **kwargs,
        )

    else:

        p.plot_bivariate_histogram(
            common_bins=common_bins,
            common_norm=common_norm,
            thresh=thresh,
            pthresh=pthresh,
            pmax=pmax,
            color=color,
            legend=legend,
            cbar=cbar,
            cbar_ax=cbar_ax,
            cbar_kws=cbar_kws,
            estimate_kws=estimate_kws,
            **kwargs,
        )

    return ax

