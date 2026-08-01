
def _build_line_series(*args, **kwargs):
    """Loop over the provided arguments and create the necessary line series.
    """
    series = []
    sum_bound = int(kwargs.get("sum_bound", 1000))
    for arg in args:
        expr, r, label, rendering_kw = arg
        kw = kwargs.copy()
        if rendering_kw is not None:
            kw["rendering_kw"] = rendering_kw
        # TODO: _process_piecewise check goes here
        if not callable(expr):
            arg = _process_summations(sum_bound, *arg)
        series.append(LineOver1DRangeSeries(*arg[:-1], **kw))
    return series

