
def test_apply_no_name_column_conflict():
    df = DataFrame(
        {
            "name": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
            "name2": [0, 0, 0, 1, 1, 1, 0, 0, 1, 1],
            "value": range(9, -1, -1),
        }
    )

    # it works! #2605
    grouped = df.groupby(["name", "name2"])
    grouped.apply(lambda x: x.sort_values("value", inplace=True))

