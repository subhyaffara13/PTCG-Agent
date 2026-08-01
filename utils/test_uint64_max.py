
def test_uint64_max():
    # Test interpolation respects uint64 max.  Reported to fail at least on
    # win32 (due to the 32 bit visual C compiler using signed int64 when
    # converting between uint64 to double) and Debian on s390x.
    # Interpolation is always done in double precision floating point, so
    # we use the largest uint64 value for which int(float(big)) still fits
    # in a uint64.
    # This test was last enabled on macOS only, and there it started failing
    # on arm64 as well (see gh-19117).
    big = 2**64 - 1025
    arr = np.array([big, big, big], dtype=np.uint64)
    # Tests geometric transform (map_coordinates, affine_transform)
    inds = np.indices(arr.shape) - 0.1
    x = ndimage.map_coordinates(arr, inds)
    assert x[1] == int(float(big))
    assert x[2] == int(float(big))
    # Tests zoom / shift
    x = ndimage.shift(arr, 0.1)
    assert x[1] == int(float(big))
    assert x[2] == int(float(big))

