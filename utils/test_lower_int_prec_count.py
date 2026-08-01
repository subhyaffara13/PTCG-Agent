
def test_lower_int_prec_count():
    df = DataFrame(
        {
            "a": np.array([0, 1, 2, 100], np.int8),
            "b": np.array([1, 2, 3, 6], np.uint32),
            "c": np.array([4, 5, 6, 8], np.int16),
            "grp": list("ab" * 2),
        }
    )
    result = df.groupby("grp").count()
    expected = DataFrame(
        {"a": [2, 2], "b": [2, 2], "c": [2, 2]}, index=Index(list("ab"), name="grp")
    )
    tm.assert_frame_equal(result, expected)

