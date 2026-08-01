
def test_patch_edgegapcolor_init():
    """Test that edgegapcolor can be passed in __init__."""
    patch = Rectangle((0, 0), 1, 1, edgegapcolor='blue')
    assert mcolors.same_color(patch.get_edgegapcolor(), 'blue')

