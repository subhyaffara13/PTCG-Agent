
def test_real_input(func, dtype, xp):
    x = xp.asarray([1, 2, 3], dtype=getattr(xp, dtype))
    # func(x) should not raise an exception
    func(x)

