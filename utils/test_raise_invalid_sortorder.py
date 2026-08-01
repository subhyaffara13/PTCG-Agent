
def test_raise_invalid_sortorder():
    # Test that the MultiIndex constructor raise when an incorrect sortorder is given
    # GH#28518

    levels = [[0, 1], [0, 1, 2]]

    # Correct sortorder
    MultiIndex(
        levels=levels, codes=[[0, 0, 0, 1, 1, 1], [0, 1, 2, 0, 1, 2]], sortorder=2
    )

    with pytest.raises(ValueError, match=r".* sortorder 2 with lexsort_depth 1.*"):
        MultiIndex(
            levels=levels, codes=[[0, 0, 0, 1, 1, 1], [0, 1, 2, 0, 2, 1]], sortorder=2
        )

    with pytest.raises(ValueError, match=r".* sortorder 1 with lexsort_depth 0.*"):
        MultiIndex(
            levels=levels, codes=[[0, 0, 1, 0, 1, 1], [0, 1, 0, 2, 2, 1]], sortorder=1
        )

