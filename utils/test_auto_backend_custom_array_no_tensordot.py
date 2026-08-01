
def test_auto_backend_custom_array_no_tensordot() -> None:
    x = ArrayShaped((1, 2, 3))
    # Shaped is an array-like object defined by opt_einsum - which has no TDOT
    assert infer_backend(x) == "opt_einsum"
    assert parse_backend([x], "auto") == "numpy"
    assert parse_backend([x], None) == "numpy"

