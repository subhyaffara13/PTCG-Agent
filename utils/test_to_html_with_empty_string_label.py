
def test_to_html_with_empty_string_label():
    # GH 3547, to_html regards empty string labels as repeated labels
    data = {"c1": ["a", "b"], "c2": ["a", ""], "data": [1, 2]}
    df = DataFrame(data).set_index(["c1", "c2"])
    result = df.to_html()
    assert "rowspan" not in result

