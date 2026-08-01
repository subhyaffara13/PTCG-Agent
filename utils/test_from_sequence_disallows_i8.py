
def test_from_sequence_disallows_i8():
    arr = period_array(["2000", "2001"], freq="D")

    msg = str(arr[0].ordinal)
    with pytest.raises(TypeError, match=msg):
        PeriodArray._from_sequence(arr.asi8, dtype=arr.dtype)

    with pytest.raises(TypeError, match=msg):
        PeriodArray._from_sequence(list(arr.asi8), dtype=arr.dtype)

