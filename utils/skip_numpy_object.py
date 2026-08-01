
def skip_numpy_object(dtype, request):
    """
    Tests for NumpyExtensionArray with nested data. Users typically won't create
    these objects via `pd.array`, but they can show up through `.array`
    on a Series with nested data. Many of the base tests fail, as they aren't
    appropriate for nested data.

    This fixture allows these tests to be skipped when used as a usefixtures
    marker to either an individual test or a test class.
    """
    if dtype == "object":
        mark = pytest.mark.xfail(reason="Fails for object dtype")
        request.applymarker(mark)

