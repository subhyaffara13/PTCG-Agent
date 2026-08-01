
def test_tricontour_non_finite_z():
    # github issue 10167.
    x = [0, 1, 0, 1]
    y = [0, 0, 1, 1]
    triang = mtri.Triangulation(x, y)
    plt.figure()

    with pytest.raises(ValueError, match='z array must not contain non-finite '
                                         'values within the triangulation'):
        plt.tricontourf(triang, [0, 1, 2, np.inf])

    with pytest.raises(ValueError, match='z array must not contain non-finite '
                                         'values within the triangulation'):
        plt.tricontourf(triang, [0, 1, 2, -np.inf])

    with pytest.raises(ValueError, match='z array must not contain non-finite '
                                         'values within the triangulation'):
        plt.tricontourf(triang, [0, 1, 2, np.nan])

    with pytest.raises(ValueError, match='z must not contain masked points '
                                         'within the triangulation'):
        plt.tricontourf(triang, np.ma.array([0, 1, 2, 3], mask=[1, 0, 0, 0]))

