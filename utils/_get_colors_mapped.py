
def _get_colors_mapped(series, colors):
    unique = series.unique()
    # unique and colors length can be differed
    # depending on slice value
    mapped = dict(zip(unique, colors))
    return [mapped[v] for v in series.values]

