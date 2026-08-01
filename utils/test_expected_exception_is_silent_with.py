
def test_expected_exception_is_silent_with():
    with raises(ValueError):
        raise ValueError()

