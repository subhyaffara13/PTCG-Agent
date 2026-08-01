
def test_invalid_cmap_n_components_zero():
    class CustomColormap(mcolors.Colormap):
        def __init__(self):
            super().__init__("custom")
            self.n_variates = 0

    with pytest.raises(ValueError, match='`n_variates` >= 1'):
        ca = mcolorizer.Colorizer(CustomColormap())

