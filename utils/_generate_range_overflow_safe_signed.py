
def _generate_range_overflow_safe_signed(
    endpoint: int, periods: int, stride: int, side: str
) -> int:
    """
    A special case for _generate_range_overflow_safe where `periods * stride`
    can be calculated without overflowing int64 bounds.
    """
    assert side in ["start", "end"]
    if side == "end":
        stride *= -1

    with np.errstate(over="raise"):
        addend = np.int64(periods) * np.int64(stride)
        try:
            # easy case with no overflows
            result = np.int64(endpoint) + addend
            if result == iNaT:
                # Putting this into a DatetimeArray/TimedeltaArray
                #  would incorrectly be interpreted as NaT
                raise OverflowError
            return int(result)
        except (FloatingPointError, OverflowError):
            # with endpoint negative and addend positive we risk
            #  FloatingPointError; with reversed signed we risk OverflowError
            pass

        # if stride and endpoint had opposite signs, then endpoint + addend
        #  should never overflow.  so they must have the same signs
        assert (stride > 0 and endpoint >= 0) or (stride < 0 and endpoint <= 0)

        if stride > 0:
            # watch out for very special case in which we just slightly
            #  exceed implementation bounds, but when passing the result to
            #  np.arange will get a result slightly within the bounds

            uresult = np.uint64(endpoint) + np.uint64(addend)
            i64max = np.uint64(i8max)
            assert uresult > i64max
            if uresult <= i64max + np.uint64(stride):
                return int(uresult)

    raise OutOfBoundsDatetime(
        f"Cannot generate range with {side}={endpoint} and periods={periods}"
    )

