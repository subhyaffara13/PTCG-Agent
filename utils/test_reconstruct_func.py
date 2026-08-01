
def test_reconstruct_func():
    # GH 28472, test to ensure reconstruct_func isn't moved;
    # This method is used by other libraries (e.g. dask)
    result = pd.core.apply.reconstruct_func("min")
    expected = (False, "min", None, None)
    tm.assert_equal(result, expected)

