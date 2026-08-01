
def _replot_ax(ax: Axes, freq: BaseOffset):
    data = getattr(ax, "_plot_data", None)

    # clear current axes and data
    # TODO #54485
    ax._plot_data = []  # type: ignore[attr-defined]
    ax.clear()

    decorate_axes(ax, freq)

    lines = []
    labels = []
    if data is not None:
        for series, plotf, kwds in data:
            series = series.copy(deep=False)
            idx = series.index.asfreq(freq, how="S")
            series.index = idx
            # TODO #54485
            ax._plot_data.append((series, plotf, kwds))  # type: ignore[attr-defined]

            # for tsplot
            if isinstance(plotf, str):
                from pandas.plotting._matplotlib import PLOT_CLASSES

                plotf = PLOT_CLASSES[plotf]._plot

            lines.append(plotf(ax, series.index._mpl_repr(), series.values, **kwds)[0])
            labels.append(pprint_thing(series.name))

    return lines, labels

