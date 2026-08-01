
def test_outer_subclass_preserve(arr):
    # for gh-8661
    class foo(np.ndarray):
        pass
    actual = np.multiply.outer(arr.view(foo), arr.view(foo))
    assert actual.__class__.__name__ == 'foo'

