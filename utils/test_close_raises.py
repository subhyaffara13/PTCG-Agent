
def test_close_raises():
    it = np.nditer(np.arange(3))
    assert_equal(next(it), 0)
    it.close()
    assert_raises(StopIteration, next, it)
    assert_raises(ValueError, getattr, it, 'operands')

