
def test_invalid() -> None:
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    with pytest.raises(ValueError, match=r"did you mean one of \['a', 'b'\] instead"):
        df.assign(c=pd.col("c").mean())
    df = pd.DataFrame({f"col_{i}": [0] for i in range(11)})
    msg = (
        "did you mean one of "
        r"\['col_0', 'col_1', 'col_2', 'col_3', "
        "'col_4', 'col_5', 'col_6', 'col_7', "
        r"'col_8', 'col_9',\.\.\.\] instead"
    )
    ""
    with pytest.raises(ValueError, match=msg):
        df.assign(c=pd.col("c").mean())

