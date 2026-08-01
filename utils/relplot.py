
def relplot(
    data=None, *,
    x=None, y=None, hue=None, size=None, style=None, units=None, weights=None,
    row=None, col=None, col_wrap=None, row_order=None, col_order=None,
    palette=None, hue_order=None, hue_norm=None,
    sizes=None, size_order=None, size_norm=None,
    markers=None, dashes=None, style_order=None,
    legend="auto", kind="scatter", height=5, aspect=1, facet_kws=None,
    **kwargs
):

    if kind == "scatter":

        Plotter = _ScatterPlotter
        func = scatterplot
        markers = True if markers is None else markers

    elif kind == "line":

        Plotter = _LinePlotter
        func = lineplot
        dashes = True if dashes is None else dashes

    else:
        err = f"Plot kind {kind} not recognized"
        raise ValueError(err)

    # Check for attempt to plot onto specific axes and warn
    if "ax" in kwargs:
        msg = (
            "relplot is a figure-level function and does not accept "
            "the `ax` parameter. You may wish to try {}".format(kind + "plot")
        )
        warnings.warn(msg, UserWarning)
        kwargs.pop("ax")

    # Use the full dataset to map the semantics
    variables = dict(x=x, y=y, hue=hue, size=size, style=style)
    if kind == "line":
        variables["units"] = units
        variables["weight"] = weights
    else:
        if units is not None:
            msg = "The `units` parameter has no effect with kind='scatter'."
            warnings.warn(msg, stacklevel=2)
        if weights is not None:
            msg = "The `weights` parameter has no effect with kind='scatter'."
            warnings.warn(msg, stacklevel=2)
    p = Plotter(
        data=data,
        variables=variables,
        legend=legend,
    )
    p.map_hue(palette=palette, order=hue_order, norm=hue_norm)
    p.map_size(sizes=sizes, order=size_order, norm=size_norm)
    p.map_style(markers=markers, dashes=dashes, order=style_order)

    # Extract the semantic mappings
    if "hue" in p.variables:
        palette = p._hue_map.lookup_table
        hue_order = p._hue_map.levels
        hue_norm = p._hue_map.norm
    else:
        palette = hue_order = hue_norm = None

    if "size" in p.variables:
        sizes = p._size_map.lookup_table
        size_order = p._size_map.levels
        size_norm = p._size_map.norm

    if "style" in p.variables:
        style_order = p._style_map.levels
        if markers:
            markers = {k: p._style_map(k, "marker") for k in style_order}
        else:
            markers = None
        if dashes:
            dashes = {k: p._style_map(k, "dashes") for k in style_order}
        else:
            dashes = None
    else:
        markers = dashes = style_order = None

    # Now extract the data that would be used to draw a single plot
    variables = p.variables
    plot_data = p.plot_data

    # Define the common plotting parameters
    plot_kws = dict(
        palette=palette, hue_order=hue_order, hue_norm=hue_norm,
        sizes=sizes, size_order=size_order, size_norm=size_norm,
        markers=markers, dashes=dashes, style_order=style_order,
        legend=False,
    )
    plot_kws.update(kwargs)
    if kind == "scatter":
        plot_kws.pop("dashes")

    # Add the grid semantics onto the plotter
    grid_variables = dict(
        x=x, y=y, row=row, col=col, hue=hue, size=size, style=style,
    )
    if kind == "line":
        grid_variables.update(units=units, weights=weights)
    p.assign_variables(data, grid_variables)

    # Define the named variables for plotting on each facet
    # Rename the variables with a leading underscore to avoid
    # collisions with faceting variable names
    plot_variables = {v: f"_{v}" for v in variables}
    if "weight" in plot_variables:
        plot_variables["weights"] = plot_variables.pop("weight")
    plot_kws.update(plot_variables)

    # Pass the row/col variables to FacetGrid with their original
    # names so that the axes titles render correctly
    for var in ["row", "col"]:
        # Handle faceting variables that lack name information
        if var in p.variables and p.variables[var] is None:
            p.variables[var] = f"_{var}_"
    grid_kws = {v: p.variables.get(v) for v in ["row", "col"]}

    # Rename the columns of the plot_data structure appropriately
    new_cols = plot_variables.copy()
    new_cols.update(grid_kws)
    full_data = p.plot_data.rename(columns=new_cols)

    # Set up the FacetGrid object
    facet_kws = {} if facet_kws is None else facet_kws.copy()
    g = FacetGrid(
        data=full_data.dropna(axis=1, how="all"),
        **grid_kws,
        col_wrap=col_wrap, row_order=row_order, col_order=col_order,
        height=height, aspect=aspect, dropna=False,
        **facet_kws
    )

    # Draw the plot
    g.map_dataframe(func, **plot_kws)

    # Label the axes, using the original variables
    # Pass "" when the variable name is None to overwrite internal variables
    g.set_axis_labels(variables.get("x") or "", variables.get("y") or "")

    if legend:
        # Replace the original plot data so the legend uses numeric data with
        # the correct type, since we force a categorical mapping above.
        p.plot_data = plot_data

        # Handle the additional non-semantic keyword arguments out here.
        # We're selective because some kwargs may be seaborn function specific
        # and not relevant to the matplotlib artists going into the legend.
        # Ideally, we will have a better solution where we don't need to re-make
        # the legend out here and will have parity with the axes-level functions.
        keys = ["c", "color", "alpha", "m", "marker"]
        if kind == "scatter":
            legend_artist = _scatter_legend_artist
            keys += ["s", "facecolor", "fc", "edgecolor", "ec", "linewidth", "lw"]
        else:
            legend_artist = partial(mpl.lines.Line2D, xdata=[], ydata=[])
            keys += [
                "markersize", "ms",
                "markeredgewidth", "mew",
                "markeredgecolor", "mec",
                "linestyle", "ls",
                "linewidth", "lw",
            ]

        common_kws = {k: v for k, v in kwargs.items() if k in keys}
        attrs = {"hue": "color", "style": None}
        if kind == "scatter":
            attrs["size"] = "s"
        elif kind == "line":
            attrs["size"] = "linewidth"
        p.add_legend_data(g.axes.flat[0], legend_artist, common_kws, attrs)
        if p.legend_data:
            g.add_legend(legend_data=p.legend_data,
                         label_order=p.legend_order,
                         title=p.legend_title,
                         adjust_subtitles=True)

    # Rename the columns of the FacetGrid's `data` attribute
    # to match the original column names
    orig_cols = {
        f"_{k}": f"_{k}_" if v is None else v for k, v in variables.items()
    }
    grid_data = g.data.rename(columns=orig_cols)
    if data is not None and (x is not None or y is not None):
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        g.data = pd.merge(
            data,
            grid_data[grid_data.columns.difference(data.columns)],
            left_index=True,
            right_index=True,
        )
    else:
        g.data = grid_data

    return g

