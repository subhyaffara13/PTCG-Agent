
def test_split_object_mixed(expand, method):
    mixed = Series(["a_b_c", np.nan, "d_e_f", True, datetime.today(), None, 1, 2.0])
    result = getattr(mixed.str, method)("_", expand=expand)
    exp = Series(
        [
            ["a", "b", "c"],
            np.nan,
            ["d", "e", "f"],
            np.nan,
            np.nan,
            None,
            np.nan,
            np.nan,
        ]
    )
    assert isinstance(result, Series)
    tm.assert_almost_equal(result, exp)

