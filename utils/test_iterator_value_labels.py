
def test_iterator_value_labels(temp_file):
    # GH 31544
    values = ["c_label", "b_label"] + ["a_label"] * 500
    df = DataFrame({f"col{k}": pd.Categorical(values, ordered=True) for k in range(2)})
    df.to_stata(temp_file, write_index=False)
    expected = pd.Index(["a_label", "b_label", "c_label"])
    with read_stata(temp_file, chunksize=100) as reader:
        for j, chunk in enumerate(reader):
            for i in range(2):
                tm.assert_index_equal(chunk.dtypes.iloc[i].categories, expected)
            tm.assert_frame_equal(chunk, df.iloc[j * 100 : (j + 1) * 100])

