
def test_interval_dtype_with_categorical(dtype):
    obj = Index([], dtype=dtype)

    cat = Categorical([], categories=obj)

    result = find_common_type([dtype, cat.dtype])
    assert result == dtype

