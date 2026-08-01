
def lag_plot(series: Series, lag: int = 1, ax: Axes | None = None, **kwds) -> Axes:
    """
    Lag plot for time series.

    A lag plot is a scatter plot of a time series against a lag of itself. It helps
    in visualizing the temporal dependence between observations by plotting the values
    at time `t` on the x-axis and the values at time `t + lag` on the y-axis.

    Parameters
    ----------
    series : Series
        The time series to visualize.
    lag : int, default 1
        Lag length of the scatter plot.
    ax : Matplotlib axis object, optional
        The matplotlib axis object to use.
    **kwds
        Matplotlib scatter method keyword arguments.

    Returns
    -------
    matplotlib.axes.Axes
        The matplotlib Axes object containing the lag plot.

    See Also
    --------
    plotting.autocorrelation_plot : Autocorrelation plot for time series.
    matplotlib.pyplot.scatter : A scatter plot of y vs. x with varying marker size
        and/or color in Matplotlib.

    Examples
    --------
    Lag plots are most commonly used to look for patterns in time series data.

    Given the following time series

    .. plot::
        :context: close-figs

        >>> np.random.seed(5)
        >>> x = np.cumsum(np.random.normal(loc=1, scale=5, size=50))
        >>> s = pd.Series(x)
        >>> s.plot()  # doctest: +SKIP

    A lag plot with ``lag=1`` returns

    .. plot::
        :context: close-figs

        >>> _ = pd.plotting.lag_plot(s, lag=1)
    """
    plot_backend = _get_plot_backend("matplotlib")
    return plot_backend.lag_plot(series=series, lag=lag, ax=ax, **kwds)


def lag_plot(series: Series, lag: int = 1, ax: Axes | None = None, **kwds) -> Axes:
    # workaround because `c='b'` is hardcoded in matplotlib's scatter method
    import matplotlib.pyplot as plt

    kwds.setdefault("c", plt.rcParams["patch.facecolor"])

    data = series.values
    y1 = data[:-lag]
    y2 = data[lag:]
    if ax is None:
        ax = plt.gca()
    ax.set_xlabel("y(t)")
    ax.set_ylabel(f"y(t + {lag})")
    ax.scatter(y1, y2, **kwds)
    return ax

