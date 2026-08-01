
def test_integer_repeat(int_func):
    rng = random.RandomState(123456789)
    fname, args, sha256 = int_func
    f = getattr(rng, fname)
    val = f(*args, size=1000000)
    if sys.byteorder != 'little':
        val = val.byteswap()
    res = hashlib.sha256(val.view(np.int8)).hexdigest()
    assert_(res == sha256)

