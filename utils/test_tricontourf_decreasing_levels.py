
def test_tricontourf_decreasing_levels():
    # github issue 5477.
    x = [0.0, 1.0, 1.0]
    y = [0.0, 0.0, 1.0]
    z = [0.2, 0.4, 0.6]
    plt.figure()
    with pytest.raises(ValueError):
        plt.tricontourf(x, y, z, [1.0, 0.0])

