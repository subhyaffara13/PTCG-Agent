
def test_hex_shorthand_notation():
    assert mcolors.same_color("#123", "#112233")
    assert mcolors.same_color("#123a", "#112233aa")

