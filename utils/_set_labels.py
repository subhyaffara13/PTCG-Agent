
def _set_labels(series, labels, rendering_kw):
    """Apply the `label` and `rendering_kw` keyword arguments to the series.
    """
    if not isinstance(labels, (list, tuple)):
        labels = [labels]
    if len(labels) > 0:
        if len(labels) == 1 and len(series) > 1:
            # if one label is provided and multiple series are being plotted,
            # set the same label to all data series. It maintains
            # back-compatibility
            labels *= len(series)
        if len(series) != len(labels):
            raise ValueError("The number of labels must be equal to the "
                "number of expressions being plotted.\nReceived "
                f"{len(series)} expressions and {len(labels)} labels")

        for s, l in zip(series, labels):
            s.label = l

    if rendering_kw:
        if isinstance(rendering_kw, dict):
            rendering_kw = [rendering_kw]
        if len(rendering_kw) == 1:
            rendering_kw *= len(series)
        elif len(series) != len(rendering_kw):
            raise ValueError("The number of rendering dictionaries must be "
                "equal to the number of expressions being plotted.\nReceived "
                f"{len(series)} expressions and {len(labels)} labels")
        for s, r in zip(series, rendering_kw):
            s.rendering_kw = r

