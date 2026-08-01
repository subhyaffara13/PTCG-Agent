
def test_apply_out_of_range(request, tz_naive_fixture, _offset):
    tz = tz_naive_fixture

    # try to create an out-of-bounds result timestamp; if we can't create
    # the offset skip
    try:
        if _offset in (BusinessHour, CustomBusinessHour):
            # Using 10000 in BusinessHour fails in tz check because of DST
            # difference
            offset = _get_offset(_offset, value=100000)
        else:
            offset = _get_offset(_offset, value=10000)

        result = Timestamp("20080101") + offset
        assert isinstance(result, datetime)
        assert result.tzinfo is None

        # Check tz is preserved
        t = Timestamp("20080101", tz=tz)
        result = t + offset
        assert isinstance(result, datetime)
        if tz is not None:
            assert t.tzinfo is not None

        if (
            isinstance(tz, tzlocal)
            and ((not IS64) or WASM)
            and _offset is not DateOffset
        ):
            # If we hit OutOfBoundsDatetime on non-64 bit machines
            # we'll drop out of the try clause before the next test
            request.applymarker(
                pytest.mark.xfail(reason="OverflowError inside tzlocal past 2038")
            )
        elif (
            isinstance(tz, tzlocal)
            and is_platform_windows()
            and _offset in (QuarterEnd, BQuarterBegin, BQuarterEnd, FY5253Quarter)
        ):
            request.applymarker(
                pytest.mark.xfail(reason="After GH#49737 t.tzinfo is None on CI")
            )
        assert str(t.tzinfo) == str(result.tzinfo), (t.tzinfo, result.tzinfo)

    except OutOfBoundsDatetime:
        pass
    except (ValueError, KeyError):
        # we are creating an invalid offset
        # so ignore
        pass

