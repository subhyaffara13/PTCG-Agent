
def test_callable_deprecate_kwarg_fail():
    msg = "((can only|cannot) concatenate)|(must be str)|(Can't convert)"

    with pytest.raises(TypeError, match=msg):
        _f3(old="hello")

