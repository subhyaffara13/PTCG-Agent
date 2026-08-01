
def test_format_descriptors_for_floating_point_types(test_func):
    assert "numpy.ndarray[numpy.float" in test_func.__doc__

