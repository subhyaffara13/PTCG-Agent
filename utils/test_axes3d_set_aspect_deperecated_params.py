
def test_axes3d_set_aspect_deperecated_params():
    """
    Test that using the deprecated 'anchor' and 'share' kwargs in
    set_aspect raises the correct warning.
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Test that providing the `anchor` parameter raises a deprecation warning.
    with pytest.warns(_api.MatplotlibDeprecationWarning, match="'anchor' parameter"):
        ax.set_aspect('equal', anchor='C')

    # Test that using the 'share' parameter is now deprecated.
    with pytest.warns(_api.MatplotlibDeprecationWarning, match="'share' parameter"):
        ax.set_aspect('equal', share=True)

    # Test that the `adjustable` parameter is correctly processed to satisfy
    # code coverage.
    ax.set_aspect('equal', adjustable='box')
    assert ax.get_adjustable() == 'box'

    ax.set_aspect('equal', adjustable='datalim')
    assert ax.get_adjustable() == 'datalim'

    with pytest.raises(ValueError, match="adjustable"):
        ax.set_aspect('equal', adjustable='invalid_value')

