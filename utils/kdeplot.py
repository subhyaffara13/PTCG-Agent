
def kdeplot(
    data=None, *, x=None, y=None, hue=None, weights=None,
    palette=None, hue_order=None, hue_norm=None, color=None, fill=None,
    multiple="layer", common_norm=True, common_grid=False, cumulative=False,
    bw_method="scott", bw_adjust=1, warn_singular=True, log_scale=None,
    levels=10, thresh=.05, gridsize=200, cut=3, clip=None,
    legend=True, cbar=False, cbar_ax=None, cbar_kws=None, ax=None,
    **kwargs,
):

    # --- Start with backwards compatability for versions < 0.11.0 ----------------

    # Handle (past) deprecation of `data2`
    if "data2" in kwargs:
        msg = "`data2` has been removed (replaced by `y`); please update your code."
        raise TypeError(msg)

    # Handle deprecation of `vertical`
    vertical = kwargs.pop("vertical", None)
    if vertical is not None:
        if vertical:
            action_taken = "assigning data to `y`."
            if x is None:
                data, y = y, data
            else:
                x, y = y, x
        else:
            action_taken = "assigning data to `x`."
        msg = textwrap.dedent(f"""\n
        The `vertical` parameter is deprecated; {action_taken}
        This will become an error in seaborn v0.14.0; please update your code.
        """)
        warnings.warn(msg, UserWarning, stacklevel=2)

    # Handle deprecation of `bw`
    bw = kwargs.pop("bw", None)
    if bw is not None:
        msg = textwrap.dedent(f"""\n
        The `bw` parameter is deprecated in favor of `bw_method` and `bw_adjust`.
        Setting `bw_method={bw}`, but please see the docs for the new parameters
        and update your code. This will become an error in seaborn v0.14.0.
        """)
        warnings.warn(msg, UserWarning, stacklevel=2)
        bw_method = bw

    # Handle deprecation of `kernel`
    if kwargs.pop("kernel", None) is not None:
        msg = textwrap.dedent("""\n
        Support for alternate kernels has been removed; using Gaussian kernel.
        This will become an error in seaborn v0.14.0; please update your code.
        """)
        warnings.warn(msg, UserWarning, stacklevel=2)

    # Handle deprecation of shade_lowest
    shade_lowest = kwargs.pop("shade_lowest", None)
    if shade_lowest is not None:
        if shade_lowest:
            thresh = 0
        msg = textwrap.dedent(f"""\n
        `shade_lowest` has been replaced by `thresh`; setting `thresh={thresh}.
        This will become an error in seaborn v0.14.0; please update your code.
        """)
        warnings.warn(msg, UserWarning, stacklevel=2)

    # Handle "soft" deprecation of shade `shade` is not really the right
    # terminology here, but unlike some of the other deprecated parameters it
    # is probably very commonly used and much hard to remove. This is therefore
    # going to be a longer process where, first, `fill` will be introduced and
    # be used throughout the documentation. In 0.12, when kwarg-only
    # enforcement hits, we can remove the shade/shade_lowest out of the
    # function signature all together and pull them out of the kwargs. Then we
    # can actually fire a FutureWarning, and eventually remove.
    shade = kwargs.pop("shade", None)
    if shade is not None:
        fill = shade
        msg = textwrap.dedent(f"""\n
        `shade` is now deprecated in favor of `fill`; setting `fill={shade}`.
        This will become an error in seaborn v0.14.0; please update your code.
        """)
        warnings.warn(msg, FutureWarning, stacklevel=2)

    # Handle `n_levels`
    # This was never in the formal API but it was processed, and appeared in an
    # example. We can treat as an alias for `levels` now and deprecate later.
    levels = kwargs.pop("n_levels", levels)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    p = _DistributionPlotter(
        data=data,
        variables=dict(x=x, y=y, hue=hue, weights=weights),
    )

    p.map_hue(palette=palette, order=hue_order, norm=hue_norm)

    if ax is None:
        ax = plt.gca()

    p._attach(ax, allowed_types=["numeric", "datetime"], log_scale=log_scale)

    method = ax.fill_between if fill else ax.plot
    color = _default_color(method, hue, color, kwargs)

    if not p.has_xy_data:
        return ax

    # Pack the kwargs for statistics.KDE
    estimate_kws = dict(
        bw_method=bw_method,
        bw_adjust=bw_adjust,
        gridsize=gridsize,
        cut=cut,
        clip=clip,
        cumulative=cumulative,
    )

    if p.univariate:

        plot_kws = kwargs.copy()

        p.plot_univariate_density(
            multiple=multiple,
            common_norm=common_norm,
            common_grid=common_grid,
            fill=fill,
            color=color,
            legend=legend,
            warn_singular=warn_singular,
            estimate_kws=estimate_kws,
            **plot_kws,
        )

    else:

        p.plot_bivariate_density(
            common_norm=common_norm,
            fill=fill,
            levels=levels,
            thresh=thresh,
            legend=legend,
            color=color,
            warn_singular=warn_singular,
            cbar=cbar,
            cbar_ax=cbar_ax,
            cbar_kws=cbar_kws,
            estimate_kws=estimate_kws,
            **kwargs,
        )

    return ax

