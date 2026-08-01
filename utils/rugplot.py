
def rugplot(
    data=None, *, x=None, y=None, hue=None, height=.025, expand_margins=True,
    palette=None, hue_order=None, hue_norm=None, legend=True, ax=None, **kwargs
):

    # A note: I think it would make sense to add multiple= to rugplot and allow
    # rugs for different hue variables to be shifted orthogonal to the data axis
    # But is this stacking, or dodging?

    # A note: if we want to add a style semantic to rugplot,
    # we could make an option that draws the rug using scatterplot

    # A note, it would also be nice to offer some kind of histogram/density
    # rugplot, since alpha blending doesn't work great in the large n regime

    # --- Start with backwards compatability for versions < 0.11.0 ----------------

    a = kwargs.pop("a", None)
    axis = kwargs.pop("axis", None)

    if a is not None:
        data = a
        msg = textwrap.dedent("""\n
        The `a` parameter has been replaced; use `x`, `y`, and/or `data` instead.
        Please update your code; This will become an error in seaborn v0.14.0.
        """)
        warnings.warn(msg, UserWarning, stacklevel=2)

    if axis is not None:
        if axis == "x":
            x = data
        elif axis == "y":
            y = data
        data = None
        msg = textwrap.dedent(f"""\n
        The `axis` parameter has been deprecated; use the `{axis}` parameter instead.
        Please update your code; this will become an error in seaborn v0.14.0.
        """)
        warnings.warn(msg, UserWarning, stacklevel=2)

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

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    p = _DistributionPlotter(
        data=data,
        variables=dict(x=x, y=y, hue=hue),
    )
    p.map_hue(palette=palette, order=hue_order, norm=hue_norm)

    if ax is None:
        ax = plt.gca()

    p._attach(ax)

    color = kwargs.pop("color", kwargs.pop("c", None))
    kwargs["color"] = _default_color(ax.plot, hue, color, kwargs)

    if not p.has_xy_data:
        return ax

    p.plot_rug(height, expand_margins, legend, **kwargs)

    return ax

