
def test_group_apply_once_per_group2(capsys):
    # GH: 31111
    # groupby-apply need to execute len(set(group_by_columns)) times

    expected = 2  # Number of times `apply` should call a function for the current test

    df = DataFrame(
        {
            "group_by_column": [0, 0, 0, 0, 1, 1, 1, 1],
            "test_column": ["0", "2", "4", "6", "8", "10", "12", "14"],
        },
        index=["0", "2", "4", "6", "8", "10", "12", "14"],
    )

    df.groupby("group_by_column", group_keys=False).apply(
        lambda df: print("function_called")
    )

    result = capsys.readouterr().out.count("function_called")
    # If `groupby` behaves unexpectedly, this test will break
    assert result == expected

