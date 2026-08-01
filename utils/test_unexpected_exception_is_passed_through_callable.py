
def test_unexpected_exception_is_passed_through_callable():
    def f():
        raise ValueError("some error message")
    try:
        raises(TypeError, f)
        assert False
    except ValueError as e:
        assert str(e) == "some error message"

