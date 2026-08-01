
def test_grouper_dropna_propagation(dropna):
    # GH 36604
    df = pd.DataFrame({"A": [0, 0, 1, None], "B": [1, 2, 3, None]})
    gb = df.groupby("A", dropna=dropna)
    assert gb._grouper.dropna == dropna

