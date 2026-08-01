
def test_scalar_fail(errors, checker):
    scalar = "fail"

    if isinstance(checker, str):
        with pytest.raises(ValueError, match=checker):
            to_numeric(scalar, errors=errors)
    else:
        assert checker(to_numeric(scalar, errors=errors))

