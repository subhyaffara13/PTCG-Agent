
def test_compare_different_shapes():
    msg = (
        r"Can only compare identically-labeled \(both index and columns\) DataFrame "
        "objects"
    )
    df1 = pd.DataFrame(np.ones((3, 3)))
    df2 = pd.DataFrame(np.zeros((2, 1)))
    with pytest.raises(ValueError, match=msg):
        df1.compare(df2)

