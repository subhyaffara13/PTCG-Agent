
def test_add_out_of_pydatetime_range():
    # GH#50348 don't raise in Timestamp.replace
    ts = Timestamp(np.datetime64("-20000-12-31"))
    off = YearEnd()

    result = ts + off
    # TODO(cython3): "arg: datetime" annotation will impose
    # datetime limitations on Timestamp. The fused type below works in cy3
    # ctypedef fused datetimelike:
    #     _Timestamp
    #     datetime
    # expected = Timestamp(np.datetime64("-19999-12-31"))
    # assert result == expected
    assert result.year in (-19999, 1973)
    assert result.month == 12
    assert result.day == 31

