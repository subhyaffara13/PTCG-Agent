
def test_multi_index_unnamed(all_parsers, index_col, columns):
    # see gh-23687
    #
    # When specifying a multi-index header, make sure that
    # we don't error just because one of the rows in our header
    # has ALL column names containing the string "Unnamed". The
    # correct condition to check is whether the row contains
    # ALL columns that did not have names (and instead were given
    # placeholder ones).
    parser = all_parsers
    header = [0, 1]

    if index_col is None:
        data = ",".join(columns or ["", ""]) + "\n0,1\n2,3\n4,5\n"
    else:
        data = ",".join([""] + (columns or ["", ""])) + "\n,0,1\n0,2,3\n1,4,5\n"

    result = parser.read_csv(StringIO(data), header=header, index_col=index_col)
    exp_columns = []

    if columns is None:
        columns = ["", "", ""]

    for i, col in enumerate(columns):
        if not col:  # Unnamed.
            col = f"Unnamed: {i if index_col is None else i + 1}_level_0"

        exp_columns.append(col)

    columns = MultiIndex.from_tuples(zip(exp_columns, ["0", "1"]))
    expected = DataFrame([[2, 3], [4, 5]], columns=columns)
    tm.assert_frame_equal(result, expected)

