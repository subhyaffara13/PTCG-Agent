
def test_reconstruct_remove_unused():
    # xref to GH 2770
    df = DataFrame(
        [["deleteMe", 1, 9], ["keepMe", 2, 9], ["keepMeToo", 3, 9]],
        columns=["first", "second", "third"],
    )
    df2 = df.set_index(["first", "second"], drop=False)
    df2 = df2[df2["first"] != "deleteMe"]

    # removed levels are there
    expected = MultiIndex(
        levels=[["deleteMe", "keepMe", "keepMeToo"], [1, 2, 3]],
        codes=[[1, 2], [1, 2]],
        names=["first", "second"],
    )
    result = df2.index
    tm.assert_index_equal(result, expected)

    expected = MultiIndex(
        levels=[["keepMe", "keepMeToo"], [2, 3]],
        codes=[[0, 1], [0, 1]],
        names=["first", "second"],
    )
    result = df2.index.remove_unused_levels()
    tm.assert_index_equal(result, expected)

    # idempotent
    result2 = result.remove_unused_levels()
    tm.assert_index_equal(result2, expected)
    assert result2.is_(result)

