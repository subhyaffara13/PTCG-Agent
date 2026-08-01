
def test_stem_polar_baseline():
    """Test that the baseline is interpolated so that it will follow the radius."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    x = np.linspace(1.57, 3.14, 10)
    y = np.linspace(0, 1, 10)
    bottom = 0.5
    container = ax.stem(x, y, bottom=bottom)
    assert container.baseline.get_path()._interpolation_steps > 100

