
def test_datetime_categorical_multikey_groupby_indices():
    # GH 26859
    df = DataFrame(
        {
            "a": Series(list("abc")),
            "b": Series(
                to_datetime(["2018-01-01", "2018-02-01", "2018-03-01"]),
                dtype="category",
            ),
            "c": Categorical.from_codes([-1, 0, 1], categories=[0, 1]),
        }
    )
    result = df.groupby(["a", "b"], observed=False).indices
    expected = {
        ("a", Timestamp("2018-01-01 00:00:00")): np.array([0]),
        ("b", Timestamp("2018-02-01 00:00:00")): np.array([1]),
        ("c", Timestamp("2018-03-01 00:00:00")): np.array([2]),
    }
    assert result == expected

