
def test_css_border_shorthand_sides(shorthand, sides):
    def create_border_dict(sides, color=None, style=None, width=None):
        resolved = {}
        for side in sides:
            if color:
                resolved[f"border-{side}-color"] = color
            if style:
                resolved[f"border-{side}-style"] = style
            if width:
                resolved[f"border-{side}-width"] = width
        return resolved

    assert_resolves(
        f"{shorthand}: 1pt red solid", create_border_dict(sides, "red", "solid", "1pt")
    )

