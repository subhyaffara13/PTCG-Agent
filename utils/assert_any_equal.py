
def assert_any_equal(output, alternatives):
    """ Assert `output` is equal to at least one element in `alternatives`
    """
    one_equal = False
    for expected in alternatives:
        if np.all(output == expected):
            one_equal = True
            break
    assert_(one_equal)

