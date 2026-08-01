
def test_validate_bool_kwarg_fail(name, value):
    msg = (
        f'For argument "{name}" expected type bool, '
        f"received type {type(value).__name__}"
    )

    with pytest.raises(ValueError, match=msg):
        validate_bool_kwarg(value, name)

