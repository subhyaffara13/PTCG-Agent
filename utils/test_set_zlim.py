
def test_set_zlim():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    assert np.allclose(ax.get_zlim(), (-1/48, 49/48))
    ax.set_zlim(zmax=2)
    assert np.allclose(ax.get_zlim(), (-1/48, 2))
    ax.set_zlim(zmin=1)
    assert ax.get_zlim() == (1, 2)

    with pytest.raises(
            TypeError, match="Cannot pass both 'lower' and 'min'"):
        ax.set_zlim(bottom=0, zmin=1)
    with pytest.raises(
            TypeError, match="Cannot pass both 'upper' and 'max'"):
        ax.set_zlim(top=0, zmax=1)

