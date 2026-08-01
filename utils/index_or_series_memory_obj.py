
def index_or_series_memory_obj(request):
    """
    Fixture for tests on indexes, series, series with a narrow dtype and
    series with empty objects type
    copy to avoid mutation, e.g. setting .name
    """
    return _index_or_series_memory_objs[request.param].copy(deep=False)

