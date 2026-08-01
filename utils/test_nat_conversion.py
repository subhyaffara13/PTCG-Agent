
def test_nat_conversion():
    for nat in [np.datetime64("NaT", "s"), np.timedelta64("NaT", "s")]:
        with pytest.raises(ValueError, match="string coercion is disabled"):
            np.array(["a", nat], dtype=StringDType(coerce=False))

