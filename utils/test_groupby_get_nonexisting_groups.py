
def test_groupby_get_nonexisting_groups():
    # GH#32492
    df = pd.DataFrame(
        data={
            "A": ["a1", "a2", None],
            "B": ["b1", "b2", "b1"],
            "val": [1, 2, 3],
        }
    )
    grps = df.groupby(by=["A", "B"])

    msg = "('a2', 'b1')"
    with pytest.raises(KeyError, match=msg):
        grps.get_group(("a2", "b1"))

