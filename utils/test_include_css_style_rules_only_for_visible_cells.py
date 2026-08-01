
def test_include_css_style_rules_only_for_visible_cells(styler_mi):
    # GH 43619
    result = (
        styler_mi.set_uuid("")
        .map(lambda v: "color: blue;")
        .hide(styler_mi.data.columns[1:], axis="columns")
        .hide(styler_mi.data.index[1:], axis="index")
        .to_html()
    )
    expected_styles = dedent(
        """\
        <style type="text/css">
        #T__row0_col0 {
          color: blue;
        }
        </style>
        """
    )
    assert expected_styles in result

