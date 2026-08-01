
def test_to_numpy_alias():
    # GH 24653: alias .to_numpy() for scalars
    expected = NaT.to_datetime64()
    result = NaT.to_numpy()

    assert isna(expected) and isna(result)

    # GH#44460
    result = NaT.to_numpy("M8[s]")
    assert isinstance(result, np.datetime64)
    assert result.dtype == "M8[s]"

    result = NaT.to_numpy("m8[ns]")
    assert isinstance(result, np.timedelta64)
    assert result.dtype == "m8[ns]"

    result = NaT.to_numpy("m8[s]")
    assert isinstance(result, np.timedelta64)
    assert result.dtype == "m8[s]"

    with pytest.raises(ValueError, match="NaT.to_numpy dtype must be a "):
        NaT.to_numpy(np.int64)

