
def test_array_dtype_short_repr(sctype):
    # Mainly test that rational/rational2 (both legacy dtypes) use short repr
    # which in the end should just be the name for these (not default dtypes).
    arr = np.zeros(1, dtype=sctype)
    res = repr(arr)
    assert f"dtype={sctype.__name__}" in res

