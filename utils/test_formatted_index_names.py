
def test_formatted_index_names(input_names, expected_names):
    # GH#60190
    df = pd.DataFrame({name: [1, 2, 3] for name in input_names}).set_index(input_names)
    formatted_names = str(df.index.names)

    assert formatted_names == expected_names

