
def test_nunique_dropna(dropna):
    # GH37566
    ser = pd.Series(["yes", "yes", pd.NA, np.nan, None, pd.NaT])
    res = ser.nunique(dropna)
    assert res == 1 if dropna else 5

