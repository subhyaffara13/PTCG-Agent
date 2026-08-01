
def test_gh_5430():
    # At least one of these raises an error unless gh-5430 is
    # fixed. In py2k an int is implemented using a C long, so
    # which one fails depends on your system. In py3k there is only
    # one arbitrary precision integer type, so both should fail.
    sigma = np.int32(1)
    out = ndimage._ni_support._normalize_sequence(sigma, 1)
    assert out == [sigma]
    sigma = np.int64(1)
    out = ndimage._ni_support._normalize_sequence(sigma, 1)
    assert out == [sigma]
    # This worked before; make sure it still works
    sigma = 1
    out = ndimage._ni_support._normalize_sequence(sigma, 1)
    assert out == [sigma]
    # This worked before; make sure it still works
    sigma = [1, 1]
    out = ndimage._ni_support._normalize_sequence(sigma, 2)
    assert out == sigma
    # Also include the OPs original example to make sure we fixed the issue
    x = np.random.normal(size=(256, 256))
    perlin = np.zeros_like(x)
    for i in 2**np.arange(6):
        perlin += ndimage.gaussian_filter(x, i, mode="wrap") * i**2
    # This also fixes gh-4106, show that the OPs example now runs.
    x = np.int64(21)
    ndimage._ni_support._normalize_sequence(x, 0)

