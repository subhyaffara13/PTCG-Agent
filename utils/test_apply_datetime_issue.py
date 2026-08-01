
def test_apply_datetime_issue(group_column_dtlike):
    # GH-28247
    # groupby-apply throws an error if one of the columns in the DataFrame
    #   is a datetime object and the column labels are different from
    #   standard int values in range(len(num_columns))

    df = DataFrame({"a": ["foo"], "b": [group_column_dtlike]})
    result = df.groupby("a").apply(lambda x: Series(["spam"], index=[42]))

    expected = DataFrame(["spam"], Index(["foo"], dtype="str", name="a"), columns=[42])
    tm.assert_frame_equal(result, expected)

