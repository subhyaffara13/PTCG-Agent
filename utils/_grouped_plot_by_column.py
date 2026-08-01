
def _grouped_plot_by_column(
    plotf,
    data,
    columns=None,
    by=None,
    numeric_only: bool = True,
    grid: bool = False,
    figsize: tuple[float, float] | None = None,
    ax=None,
    layout=None,
    return_type=None,
    **kwargs,
):
    grouped = data.groupby(by, observed=False)
    if columns is None:
        if not isinstance(by, (list, tuple)):
            by = [by]
        columns = data._get_numeric_data().columns.difference(by)
    naxes = len(columns)
    fig, axes = create_subplots(
        naxes=naxes,
        sharex=kwargs.pop("sharex", True),
        sharey=kwargs.pop("sharey", True),
        figsize=figsize,
        ax=ax,
        layout=layout,
    )

    # GH 45465: move the "by" label based on "vert"
    xlabel, ylabel = kwargs.pop("xlabel", None), kwargs.pop("ylabel", None)
    if kwargs.get("vert", True):
        xlabel = xlabel or by
    else:
        ylabel = ylabel or by

    ax_values = []

    for ax, col in zip(flatten_axes(axes), columns, strict=False):
        gp_col = grouped[col]
        keys, values = zip(*gp_col, strict=True)
        re_plotf = plotf(keys, values, ax, xlabel=xlabel, ylabel=ylabel, **kwargs)
        ax.set_title(col)
        ax_values.append(re_plotf)
        ax.grid(grid)

    result = pd.Series(ax_values, index=columns, copy=False)

    # Return axes in multiplot case, maybe revisit later # 985
    if return_type is None:
        result = axes

    byline = by[0] if len(by) == 1 else by
    fig.suptitle(f"Boxplot grouped by {byline}")
    maybe_adjust_figure(fig, bottom=0.15, top=0.9, left=0.1, right=0.9, wspace=0.2)

    return result

