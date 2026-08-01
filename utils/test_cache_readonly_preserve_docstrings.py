
def test_cache_readonly_preserve_docstrings():
    # GH18197
    assert Index.hasnans.__doc__ is not None

