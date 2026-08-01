
def test_numpy_type_funcs(idx, func):
    msg = (
        f"ufunc '{func.__name__}' not supported for the input types, and the inputs "
        "could not be safely coerced to any supported types according to "
        "the casting rule ''safe''"
    )
    with pytest.raises(TypeError, match=msg):
        func(idx)

