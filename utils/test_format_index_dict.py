
def test_format_index_dict(styler):
    ctx = styler.format_index({0: lambda v: v.upper()})._translate(True, True)
    for i, val in enumerate(["X", "Y"]):
        assert ctx["body"][i][0]["display_value"] == val

