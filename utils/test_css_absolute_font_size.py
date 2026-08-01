
def test_css_absolute_font_size(size, relative_to, resolved):
    if relative_to is None:
        inherited = None
    else:
        inherited = {"font-size": relative_to}
    assert_resolves(f"font-size: {size}", {"font-size": resolved}, inherited=inherited)

