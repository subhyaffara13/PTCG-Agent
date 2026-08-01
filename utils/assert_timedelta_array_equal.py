
def assert_timedelta_array_equal(
    left, right, obj: str = "TimedeltaArray", check_freq: bool = True
) -> None:
    __tracebackhide__ = True
    _check_isinstance(left, right, TimedeltaArray)
    assert_numpy_array_equal(left._ndarray, right._ndarray, obj=f"{obj}._ndarray")
    if check_freq:
        assert_attr_equal("freq", left, right, obj=obj)

