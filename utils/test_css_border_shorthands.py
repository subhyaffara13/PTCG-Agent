
def test_css_border_shorthands(prop, expected):
    color, style, width = expected

    assert_resolves(
        f"border-left: {prop}",
        {
            "border-left-color": color,
            "border-left-style": style,
            "border-left-width": width,
        },
    )

