
def test_integer_dtype(int_func):
    random.seed(123456789)
    fname, args, sha256 = int_func
    f = getattr(random, fname)
    actual = f(*args, size=2)
    assert_(actual.dtype == np.dtype('l'))

