
def test_is_string_dtype_nullable(nullable_string_dtype):
    assert com.is_string_dtype(pd.array(["a", "b"], dtype=nullable_string_dtype))

