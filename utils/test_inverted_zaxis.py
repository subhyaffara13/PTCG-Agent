
def test_inverted_zaxis():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_zlim(0, 1)
    assert not ax.zaxis_inverted()
    assert ax.get_zlim() == (0, 1)
    assert ax.get_zbound() == (0, 1)

    # Change bound
    ax.set_zbound((0, 2))
    assert not ax.zaxis_inverted()
    assert ax.get_zlim() == (0, 2)
    assert ax.get_zbound() == (0, 2)

    # Change invert
    ax.invert_zaxis()
    assert ax.zaxis_inverted()
    assert ax.get_zlim() == (2, 0)
    assert ax.get_zbound() == (0, 2)

    # Set upper bound
    ax.set_zbound(upper=1)
    assert ax.zaxis_inverted()
    assert ax.get_zlim() == (1, 0)
    assert ax.get_zbound() == (0, 1)

    # Set lower bound
    ax.set_zbound(lower=2)
    assert ax.zaxis_inverted()
    assert ax.get_zlim() == (2, 1)
    assert ax.get_zbound() == (1, 2)

