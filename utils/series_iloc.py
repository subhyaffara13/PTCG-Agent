
def series_iloc(series):
    def get(series):
        return _iLocIndexer(series)

    return get

