
def nonfunctional_tooslow(func):
    return pytest.mark.skip(
        reason="    Test not yet functional (too slow), needs more work."
    )(func)

