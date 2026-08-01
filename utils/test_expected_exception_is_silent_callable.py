
def test_expected_exception_is_silent_callable():
    def f():
        raise ValueError()
    raises(ValueError, f)

