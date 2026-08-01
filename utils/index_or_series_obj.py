
def index_or_series_obj(request):
    """
    Fixture for tests on indexes, series and series with a narrow dtype
    copy to avoid mutation, e.g. setting .name
    """
    return _index_or_series_objs[request.param].copy(deep=False)

