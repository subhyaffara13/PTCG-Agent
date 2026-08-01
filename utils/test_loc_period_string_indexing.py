
def test_loc_period_string_indexing():
    # GH 9892
    a = pd.period_range("2013Q1", "2013Q4", freq="Q")
    i = (1111, 2222, 3333)
    idx = MultiIndex.from_product((a, i), names=("Period", "CVR"))
    df = DataFrame(
        index=idx,
        columns=(
            "OMS",
            "OMK",
            "RES",
            "DRIFT_IND",
            "OEVRIG_IND",
            "FIN_IND",
            "VARE_UD",
            "LOEN_UD",
            "FIN_UD",
        ),
    )
    result = df.loc[("2013Q1", 1111), "OMS"]

    alt = df.loc[(a[0], 1111), "OMS"]
    assert np.isnan(alt)

    # Because the resolution of the string matches, it is an exact lookup,
    #  not a slice
    assert np.isnan(result)

    alt = df.loc[("2013Q1", 1111), "OMS"]
    assert np.isnan(alt)

