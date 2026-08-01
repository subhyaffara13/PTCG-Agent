
def frame_or_series(request):
    """
    Fixture to parametrize over DataFrame and Series.
    """
    return request.param

