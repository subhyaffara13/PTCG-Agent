
def test_doc(func):
    """xp_capabilities updates the docstring in place. 
    Make sure it does so exactly once, including when SCIPY_ARRAY_API is not set.
    """
    match = "has experimental support for Python Array API"
    assert func.__doc__.count(match) == 1

