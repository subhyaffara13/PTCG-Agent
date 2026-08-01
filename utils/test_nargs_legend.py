
def test_nargs_legend():
    with pytest.raises(TypeError, match='3 were given'):
        ax = plt.subplot()
        # legend() takes 0-2 arguments.
        ax.legend(['First'], ['Second'], 3)

