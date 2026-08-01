
def test_parse_latex_table_styles(styler):
    styler.set_table_styles(
        [
            {"selector": "foo", "props": [("attr", "value")]},
            {"selector": "bar", "props": [("attr", "overwritten")]},
            {"selector": "bar", "props": [("attr", "baz"), ("attr2", "ignored")]},
            {"selector": "label", "props": [("", "{fig§item}")]},
        ]
    )
    assert _parse_latex_table_styles(styler.table_styles, "bar") == "baz"

    # test '§' replaced by ':' [for CSS compatibility]
    assert _parse_latex_table_styles(styler.table_styles, "label") == "{fig:item}"

