
def test_numpy_random_permute(dtype, box):
    # https://github.com/pandas-dev/pandas/issues/63935
    arr = box(["a", "bb", "ccc"], dtype=dtype)

    rng = np.random.default_rng(2)
    result = rng.permutation(arr)
    assert isinstance(result, np.ndarray)
    assert sorted(result.tolist()) == ["a", "bb", "ccc"]

