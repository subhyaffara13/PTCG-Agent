
def test_nargs_stem():
    with pytest.raises(TypeError, match='0 were given'):
        # stem() takes 1-3 arguments.
        plt.stem()

