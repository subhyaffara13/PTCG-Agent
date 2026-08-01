
def test_distutils_has_origin():
    """
    Distutils module spec should have an origin. #2990.
    """
    assert __import__('distutils').__spec__.origin

