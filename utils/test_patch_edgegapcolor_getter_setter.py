
def test_patch_edgegapcolor_getter_setter():
    """Test that edgegapcolor can be set and retrieved."""
    patch = Rectangle((0, 0), 1, 1)
    # Default is None
    assert patch.get_edgegapcolor() is None

    # Set to a color
    patch.set_edgegapcolor('red')
    assert mcolors.same_color(patch.get_edgegapcolor(), 'red')

    # Set back to None
    patch.set_edgegapcolor(None)
    assert patch.get_edgegapcolor() is None

