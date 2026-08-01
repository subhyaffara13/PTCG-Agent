
def test_threaded_same(x, func, workers):
    expected = func(x, workers=1)
    actual = func(x, workers=workers)
    assert_allclose(actual, expected)

