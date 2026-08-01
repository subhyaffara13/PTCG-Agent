
def test_masked_array_2_sentinel_array():
    # prepare arrays
    rng = np.random.default_rng(805715284)
    A = rng.random((10, 11, 12))
    B = rng.random(12)
    mask = A < 0.5
    A = np.ma.masked_array(A, mask)

    # set arbitrary elements to special values
    # (these values might have been considered for use as sentinel values)
    max_float = np.finfo(np.float64).max
    max_float2 = np.nextafter(max_float, -np.inf)
    max_float3 = np.nextafter(max_float2, -np.inf)
    A[3, 4, 1] = np.nan
    A[4, 5, 2] = np.inf
    A[5, 6, 3] = max_float
    B[8] = np.nan
    B[7] = np.inf
    B[6] = max_float2

    # convert masked A to array with sentinel value, don't modify B
    out_arrays, sentinel = _masked_arrays_2_sentinel_arrays([A, B])
    A_out, B_out = out_arrays

    # check that good sentinel value was chosen (according to intended logic)
    assert (sentinel != max_float) and (sentinel != max_float2)
    assert sentinel == max_float3

    # check that output arrays are as intended
    A_reference = A.data
    A_reference[A.mask] = sentinel
    np.testing.assert_array_equal(A_out, A_reference)
    assert B_out is B

