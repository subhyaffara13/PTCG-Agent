
def test_arithmetic_ops(all_arithmetic_functions, other):
    op = all_arithmetic_functions

    if op.__name__ in ("pow", "rpow", "rmod") and isinstance(other, (str, bytes)):
        pytest.skip(reason=f"{op.__name__} with NA and {other} not defined.")
    if op.__name__ in ("divmod", "rdivmod"):
        assert op(NA, other) is (NA, NA)
    else:
        if op.__name__ == "rpow":
            # avoid special case
            other += 1
        assert op(NA, other) is NA

