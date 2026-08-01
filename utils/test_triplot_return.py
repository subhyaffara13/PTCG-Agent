
def test_triplot_return():
    # Check that triplot returns the artists it adds
    ax = plt.figure().add_subplot()
    triang = mtri.Triangulation(
        [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0, 1.0],
        triangles=[[0, 1, 3], [3, 2, 0]])
    assert ax.triplot(triang, "b-") is not None, \
        'triplot should return the artist it adds'

