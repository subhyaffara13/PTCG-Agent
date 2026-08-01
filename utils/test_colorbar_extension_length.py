
def test_colorbar_extension_length():
    """Test variable length colorbar extensions."""
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    # Create figures for uniform and proportionally spaced colorbars.
    _colorbar_extension_length('uniform')
    _colorbar_extension_length('proportional')

