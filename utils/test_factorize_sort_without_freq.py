
def test_factorize_sort_without_freq():
    dta = DatetimeArray._from_sequence([0, 2, 1], dtype="M8[ns]")

    msg = r"call pd.factorize\(obj, sort=True\) instead"
    with pytest.raises(NotImplementedError, match=msg):
        dta.factorize(sort=True)

    # Do TimedeltaArray while we're here
    tda = dta - dta[0]
    with pytest.raises(NotImplementedError, match=msg):
        tda.factorize(sort=True)

