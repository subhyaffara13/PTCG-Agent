
def test_convert_value(temp_h5_path, where: str, expected):
    # GH39420
    # Check that read_hdf with categorical columns can filter by where condition.
    df = DataFrame({"col": ["a", "b", "s"]})
    df.col = df.col.astype("category")
    max_widths = {"col": 1}
    categorical_values = sorted(df.col.unique())
    expected = DataFrame({"col": expected})
    expected.col = expected.col.astype("category")
    expected.col = expected.col.cat.set_categories(categorical_values)

    df.to_hdf(temp_h5_path, key="df", format="table", min_itemsize=max_widths)
    result = read_hdf(temp_h5_path, where=f'col=="{where}"')
    tm.assert_frame_equal(result, expected)

