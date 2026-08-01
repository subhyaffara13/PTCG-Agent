
def test_validate_n_error():
    with pytest.raises(TypeError, match="argument must be an integer"):
        DateOffset(n="Doh!")

    with pytest.raises(TypeError, match="argument must be an integer"):
        MonthBegin(n=timedelta(1))

    with pytest.raises(TypeError, match="argument must be an integer"):
        BDay(n=np.array([1, 2], dtype=np.int64))

