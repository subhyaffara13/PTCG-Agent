
def test_construct_from_td64_with_unit():
    # ignore the unit, as it may cause silently overflows leading to incorrect
    #  results, and in non-overflow cases is irrelevant GH#46827
    obj = np.timedelta64(123456789000000000, "h")

    msg = "The 'unit' keyword is only used when the Timedelta input is"

    with pytest.raises(OutOfBoundsTimedelta, match="123456789000000000 hours"):
        with tm.assert_produces_warning(UserWarning, match=msg):
            Timedelta(obj, unit="ps")

    with pytest.raises(OutOfBoundsTimedelta, match="123456789000000000 hours"):
        with tm.assert_produces_warning(UserWarning, match=msg):
            Timedelta(obj, unit="ns")

    with pytest.raises(OutOfBoundsTimedelta, match="123456789000000000 hours"):
        Timedelta(obj)

