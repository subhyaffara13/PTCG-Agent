
def test_include_css_style_rules_only_for_visible_column_labels(styler_mi):
    # GH 43619
    result = (
        styler_mi.set_uuid("")
        .map_index(lambda v: "color: blue;", axis="columns")
        .hide(styler_mi.data.columns[1:], axis="columns")
        .hide(styler_mi.data.index, axis="index")
        .to_html()
    )
    expected_styles = dedent(
        """\
        <style type="text/css">
        #T__level0_col0, #T__level1_col0 {
          color: blue;
        }
        </style>
        """
    )
    assert expected_styles in result

