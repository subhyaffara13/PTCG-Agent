
def test_tooltip_css_class(styler):
    # GH 21266
    result = styler.set_tooltips(
        DataFrame([["tooltip"]], index=["x"], columns=["A"]),
        css_class="other-class",
        props=[("color", "green")],
    ).to_html()
    assert "#T_ .other-class {\n  color: green;\n" in result
    assert '#T_ #T__row0_col0 .other-class::after {\n  content: "tooltip";\n' in result

    # GH 39563
    result = styler.set_tooltips(  # set_tooltips overwrites previous
        DataFrame([["tooltip"]], index=["x"], columns=["A"]),
        css_class="another-class",
        props="color:green;color:red;",
    ).to_html()
    assert "#T_ .another-class {\n  color: green;\n  color: red;\n}" in result

