
def _create_series(index):
    """Helper for the _series dict"""
    size = len(index)
    data = np.random.default_rng(2).standard_normal(size)
    return Series(data, index=index, name="a", copy=False)


def _create_series(series_type, plot_expr, **kwargs):
    """Extract the rendering_kw dictionary from the provided arguments and
    create an appropriate data series.
    """
    series = []
    for args in plot_expr:
        kw = kwargs.copy()
        if args[-1] is not None:
            kw["rendering_kw"] = args[-1]
        series.append(series_type(*args[:-1], **kw))
    return series

