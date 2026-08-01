
def test_to_html_columns_arg(float_frame):
    result = float_frame.to_html(columns=["A"])
    assert "<th>B</th>" not in result

