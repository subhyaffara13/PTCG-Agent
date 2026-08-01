
def test_to_html_truncation_index_false_max_cols(
    datapath, index, col_index_named, expected_output
):
    # GH 22783
    data = [
        [1.764052, 0.400157, 0.978738, 2.240893, 1.867558],
        [-0.977278, 0.950088, -0.151357, -0.103219, 0.410599],
    ]
    df = DataFrame(data)
    if col_index_named:
        df.columns.rename("columns.name", inplace=True)
    result = df.to_html(max_cols=4, index=index)
    expected = expected_html(datapath, expected_output)
    assert result == expected

