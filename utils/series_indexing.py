
def series_indexing(series, item):
    if isinstance(series, SeriesType):

        def series_getitem(series, item):
            loc = series.index.get_loc(item)
            return series.iloc[loc]

        return series_getitem

