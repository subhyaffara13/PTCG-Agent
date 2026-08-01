
def test_patch_edgegapcolor_update_from():
    """Test that edgegapcolor is copied in update_from."""
    patch1 = Rectangle((0, 0), 1, 1, edgegapcolor='green')
    patch2 = Rectangle((1, 1), 2, 2)

    patch2.update_from(patch1)
    assert mcolors.same_color(patch2.get_edgegapcolor(), 'green')

