
def test_issue_13924():
    if not numpy:
        skip("numpy not installed.")

    a = sympify(numpy.array([1]))
    assert isinstance(a, ImmutableDenseNDimArray)
    assert a[0] == 1

