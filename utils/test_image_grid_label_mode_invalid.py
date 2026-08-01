
def test_image_grid_label_mode_invalid():
    fig = plt.figure()
    with pytest.raises(ValueError, match="'foo' is not a valid value for mode"):
        ImageGrid(fig, (0, 0, 1, 1), (2, 1), label_mode="foo")

