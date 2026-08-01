
def test_custom_table_styles(styler):
    styler.set_table_styles(
        [
            {"selector": "mycommand", "props": ":{myoptions}"},
            {"selector": "mycommand2", "props": ":{myoptions2}"},
        ]
    )
    expected = dedent(
        """\
        \\begin{table}
        \\mycommand{myoptions}
        \\mycommand2{myoptions2}
        """
    )
    assert expected in styler.to_latex()

