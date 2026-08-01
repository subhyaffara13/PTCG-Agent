
def index_or_series_or_array(request):
    """
    Fixture to parametrize over Index, Series, and ExtensionArray
    """
    return request.param

