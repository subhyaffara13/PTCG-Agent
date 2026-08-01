
def test_map_dtype_inference_overflows():
    # GH#44609 case where we have to upcast
    idx = Index(np.array([1, 2, 3], dtype=np.int8))
    result = idx.map(lambda x: x * 1000)
    # TODO: we could plausibly try to infer down to int16 here
    expected = Index([1000, 2000, 3000], dtype=np.int64)
    tm.assert_index_equal(result, expected)

