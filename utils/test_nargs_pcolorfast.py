
def test_nargs_pcolorfast():
    with pytest.raises(TypeError, match='2 were given'):
        ax = plt.subplot()
        # pcolorfast() takes 1 or 3 arguments,
        # not passing any arguments fails at C = args[-1]
        # before nargs_err is raised.
        ax.pcolorfast([(0, 1), (0, 2)], [[1, 2, 3], [1, 2, 3]])

