
def test_error(data, msg):
    ser = Series(data)

    with pytest.raises(ValueError, match=msg):
        to_numeric(ser, errors="raise")


def test_error():
    df = pd.DataFrame(
        {"A": pd.Series([[0, 1, 2], np.nan, [], (3, 4)], index=list("abcd")), "B": 1}
    )
    with pytest.raises(
        ValueError, match="column must be a scalar, tuple, or list thereof"
    ):
        df.explode([list("AA")])

    with pytest.raises(ValueError, match="column must be unique"):
        df.explode(list("AA"))

    df.columns = list("AA")
    with pytest.raises(
        ValueError,
        match=re.escape("DataFrame columns must be unique. Duplicate columns: ['A']"),
    ):
        df.explode("A")

